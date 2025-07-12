from .._resource import (
    app,
    configs,
    chat
)
from Markdown import markdown_to_image, get_style_names
from fastapi import (
    HTTPException,
    BackgroundTasks,
    Form,
    Request
)
from fastapi.responses import JSONResponse
import asyncio
import os
import time
from loguru import logger
from uuid import uuid4
from pathlib import Path

@app.post("/render/{user_id}")
async def render(
    request: Request,
    background_tasks: BackgroundTasks,
    user_id: str,
    text: str = Form(...),
    style: str | None = Form(None),
    timeout: float | None = Form(None),
):
    """
    Endpoint for rendering markdown text to image
    """

    if text == None:
        raise HTTPException(status_code=400, detail="text is required")
    
    # 生成图片ID
    fuuid = uuid4()
    filename = f"{fuuid}.png"
    rendered_image_dir = configs.get_config("rendered_image_dir", "./temp/render").get_value(Path)

    # 延迟删除函数
    async def _wait_delete(sleep_time: float, filename: str):
        """
        等待一段时间后删除图片
        """
        async def _delete(filename: str):
            """
            删除图片
            """
            await asyncio.to_thread(os.remove, rendered_image_dir / filename)
            logger.info(f'Deleted image {filename}', user_id = user_id)
        
        try:
            await asyncio.sleep(sleep_time)
            await _delete(filename)
        except asyncio.CancelledError:
            logger.info("Image delete task cancelled", user_id = user_id)
            await _delete(filename)
        
    if style:
        if style not in get_style_names():
            raise HTTPException(status_code=400, detail="Invalid style")
    else:
        # 获取用户配置
        config = await chat.user_config_manager.load(user_id)
        # 获取环境变量中的图片渲染风格
        default_style = configs.get_config("markdown_to_image_style", "light").get_value(str)
        # 获取图片渲染风格
        style = config.get('render_style', default_style)
    
    if not timeout:
        timeout = configs.get_config("rendered_default_image_timeout", 60.0).get_value(float)
    
    # 日志打印文件名和渲染风格
    logger.info(f'Rendering image {filename} for "{style}" style', user_id=user_id)

    # 调用markdown_to_image函数生成图片
    await markdown_to_image(
        markdown_text = text,
        output_path = rendered_image_dir / filename,
        style = style,
        preprocess_map = configs.get_config("markdown_to_image_preprocess_map", {}).get_value(dict),
    )
    create_ms = time.time_ns() // 10**6
    create = create_ms // 1000
    logger.info(f'Created image {filename}', user_id = user_id)

    # 添加一个后台任务，时间到后删除图片
    background_tasks.add_task(_wait_delete, timeout, filename)

    # 生成图片的URL
    fileurl = request.url_for("render_file", file_uuid=fuuid)

    return JSONResponse(
        {
            "image_url": str(fileurl),
            "file_uuid": str(fuuid),
            "style": style,
            "timeout": timeout,
            "text": text,
            "created": create,
            "created_ms": create_ms
        }
    )

@app.get("/render_styles")
async def get_render_styles():
    style_names = await get_style_names()
    return JSONResponse(style_names)