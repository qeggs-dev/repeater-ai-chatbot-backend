from .._resource import (
    app,
    chat
)
from Markdown import markdown_to_image, Styles
from fastapi import (
    HTTPException,
    BackgroundTasks,
    Request
)
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import asyncio
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

    if render_request.text == None:
        raise HTTPException(status_code=400, detail="text is required")
    
    # 生成图片ID
    fuuid = uuid4()
    filename = f"{fuuid}.png"
    render_output_image_dir = Path(ConfigManager.get_configs().render.markdown.to_image.output_dir)

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
        
    if render_request.style:
        style_path = ConfigManager.get_configs().render.markdown.to_image.styles_dir
        styles = Styles(
            style_path
        )
        if render_request.style in styles.get_style_names():
            style = render_request.style
        else:
            raise HTTPException(status_code=400, detail="Invalid style")
    else:
        # 获取用户配置
        config = await chat.user_config_manager.load(user_id)
        # 获取环境变量中的图片渲染风格
        default_style = ConfigManager.get_configs().render.markdown.to_image.default_style
        # 获取图片渲染风格
        style: str = config.get('render_style', default_style)
    
    if not render_request.timeout:
        render_request.timeout = ConfigManager.get_configs().render.default_image_timeout
    
    # 日志打印文件名和渲染风格
    logger.info(f'Rendering image {filename} for "{style}" style', user_id=user_id)

    wkhtmltoimage_path = Path(ConfigManager.get_configs().render.markdown.to_image.wkhtmltoimage_path)
    style_file_encoding = ConfigManager.get_configs().render.markdown.to_image.style_file_encoding
    preprocess_map_before = ConfigManager.get_configs().render.markdown.to_image.preprocess_map.before
    preprocess_map_end = ConfigManager.get_configs().render.markdown.to_image.preprocess_map.after

    # 调用markdown_to_image函数生成图片
    await markdown_to_image(
        markdown_text = render_request.text,
        output_path = render_output_image_dir / filename,
        wkhtmltoimage_path = wkhtmltoimage_path,
        style = style,
        style_file_encoding = style_file_encoding,
        preprocess_map_before = preprocess_map_before,
        preprocess_map_end = preprocess_map_end,
    )
    create_ms = time.time_ns() // 10**6
    create = create_ms // 1000
    logger.info(f'Created image {filename}', user_id = user_id)

    # 添加一个后台任务，时间到后删除图片
    background_tasks.add_task(_wait_delete, render_request.timeout, filename)

    # 生成图片的URL
    fileurl = request.url_for("render_file", file_uuid=fuuid)

    return JSONResponse(
        {
            "image_url": str(fileurl),
            "file_uuid": str(fuuid),
            "style": style,
            "timeout": render_request.timeout,
            "text": render_request.text,
            "created": create,
            "created_ms": create_ms
        }
    )

@app.get("/render_styles")
async def get_render_styles():
    styles_path = Path(ConfigManager.get_configs().render.markdown.to_image.styles_dir)
    styles = Styles(
        styles_path = styles_path,
    )
    style_names = styles.get_style_names()
    return JSONResponse(style_names)