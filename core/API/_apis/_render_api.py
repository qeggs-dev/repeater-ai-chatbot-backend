from .._resource import (
    app,
    chat,
    browser_pool_manager
)
from ...Markdown_Render import (
    markdown_to_html,
    Styles,
    HTML_Render
)
from fastapi import (
    HTTPException,
    BackgroundTasks,
    Request
)
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
import asyncio
import aiofiles
import os
import time
from loguru import logger
from uuid import uuid4
from pathlib import Path
from ...Global_Config_Manager import ConfigManager

class RenderRequest(BaseModel):
    text: str
    style: str | None = None
    timeout: float | None = None
    css: str | None = None
    width: int | None = None
    height: int | None = None
    quality: int | None = None

@app.post("/render/{user_id}")
async def render(
    request: Request,
    background_tasks: BackgroundTasks,
    user_id: str,
    render_request:RenderRequest
):
    """
    Endpoint for rendering markdown text to image
    """
    start_time = time.monotonic_ns()

    if render_request.text == None:
        raise HTTPException(status_code=400, detail="text is required")
    
    # 生成图片ID
    fuuid = uuid4()
    filename = f"{fuuid}{ConfigManager.get_configs().render.to_image.output_suffix}"
    render_output_image_dir = Path(ConfigManager.get_configs().render.to_image.output_dir)

    # 延迟删除函数
    async def _wait_delete(sleep_time: float, filename: str):
        """
        等待一段时间后删除图片
        """
        async def _delete(filename: str):
            """
            删除图片
            """
            await asyncio.to_thread(os.remove, render_output_image_dir / filename)
            logger.info(f'Deleted image {filename}', user_id = user_id)
        
        try:
            await asyncio.sleep(sleep_time)
            await _delete(filename)
        except asyncio.CancelledError:
            logger.info("Image delete task cancelled", user_id = user_id)
            await _delete(filename)
        
    style_path = ConfigManager.get_configs().render.markdown.styles_dir
    styles = Styles(
        style_path
    )
    style_file_encoding = ConfigManager.get_configs().render.markdown.style_file_encoding

    # 获取用户配置
    config = await chat.user_config_manager.load(user_id)

    if render_request.css:
        style_name = "custom"
        css = render_request.css
    elif render_request.style:
        if render_request.style in styles.get_style_names():
            style_name = render_request.style
        else:
            raise HTTPException(
                status_code=404,
                detail="Style not found"
            )
        
        css = await styles.get_style(
            style_name,
            encoding = style_file_encoding
        )
    else:
        # 获取全局配置中的默认图片渲染风格
        style_name = ConfigManager.get_configs().render.markdown.default_style
        css = await styles.get_style(
            config.render_style or style_name,
            encoding = style_file_encoding
        )
    
    if not render_request.timeout:
        render_request.timeout = ConfigManager.get_configs().render.default_image_timeout
    
    # 日志打印文件名和渲染风格
    logger.info(f'Rendering image {filename} for "{style_name}" style', user_id=user_id)

    browser_type = ConfigManager.get_configs().render.to_image.browser_type
    preprocess_map_before = ConfigManager.get_configs().render.markdown.preprocess_map.before
    preprocess_map_after = ConfigManager.get_configs().render.markdown.preprocess_map.after
    html_template_dir = Path(ConfigManager.get_configs().render.markdown.html_template_dir)
    html_template_encoding = ConfigManager.get_configs().render.markdown.html_template_file_encoding
    html_template_name = config.render_html_template if config.render_html_template is not None else ConfigManager.get_configs().render.markdown.default_html_template
    title = config.render_title if config.render_title is not None else ConfigManager.get_configs().render.markdown.title

    width = render_request.width if render_request.width is not None else ConfigManager.get_configs().render.to_image.width
    height = render_request.height if render_request.height is not None else ConfigManager.get_configs().render.to_image.height
    quality = render_request.quality if render_request.quality is not None else ConfigManager.get_configs().render.to_image.quality

    # 读取HTML模板
    async with aiofiles.open(html_template_dir / html_template_name, 'r', encoding=html_template_encoding) as f:
        html_template = await f.read()
    
    end_of_preprocessing = time.monotonic_ns()

    # 调用生成HTML
    html = await markdown_to_html(
        markdown_text = render_request.text,
        html_template = html_template,
        width = width,
        title = title,
        css = css,
        preprocess_map_before = preprocess_map_before,
        preprocess_map_after = preprocess_map_after,
    )

    end_of_md_to_html = time.monotonic_ns()

    # 生成图片
    result = await browser_pool_manager.render_html(
        html_content = html,
        output_path = render_output_image_dir / filename,
        browser_type = browser_type,
        config = HTML_Render.RenderConfig(
            width = width,
            height = height,
            quality = quality
        )
    )

    end_of_render = time.monotonic_ns()

    create_ms = time.time_ns() // 10**6
    create = create_ms // 1000
    logger.info(f'Created image {filename}', user_id = user_id)

    # 添加一个后台任务，时间到后删除图片
    background_tasks.add_task(_wait_delete, render_request.timeout, filename)

    # 生成图片的URL
    fileurl = request.url_for("render_file", file_uuid=fuuid)

    return ORJSONResponse(
        {
            "image_url": str(fileurl),
            "file_uuid": str(fuuid),
            "style": style_name,
            "status": result.status.value,
            "browser_used": result.browser_used,
            "timeout": render_request.timeout,
            "error": result.error,
            "text": render_request.text,
            "image_render_time_ms": result.render_time_ms,
            "created": create,
            "created_ms": create_ms,
            "times": {
                "preprocess": end_of_preprocessing - start_time,
                "markdown_to_html": end_of_md_to_html - end_of_preprocessing,
                "render": end_of_render - end_of_md_to_html,
            }
        }
    )

@app.get("/render_styles")
async def get_render_styles():
    styles_path = Path(ConfigManager.get_configs().render.markdown.styles_dir)
    styles = Styles(
        styles_path = styles_path,
    )
    style_names = styles.get_style_names()
    return ORJSONResponse(style_names)