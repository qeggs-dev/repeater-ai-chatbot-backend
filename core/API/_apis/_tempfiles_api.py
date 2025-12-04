from .._resource import app, chat
from PathProcessors import validate_path
from fastapi import HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

from ...Global_Config_Manager import ConfigManager

@app.get("/file/render/{file_uuid}.png", name = "render_file")
async def get_render_file(file_uuid: str):
    """
    Endpoint for rendering file

    Args:
        file_uuid (str): The UUID of the file to render
    """
    render_output_image_dir = Path(ConfigManager.get_configs().render.to_image.output_dir)
    # 防止遍历攻击
    if not validate_path(render_output_image_dir, file_uuid):
        raise HTTPException(status_code=403, detail="Invalid file path")
    
    # 检查文件是否存在
    if not (render_output_image_dir / f"{file_uuid}.png").exists():
        raise HTTPException(detail="File not found", status_code=404)
    
    # 返回文件
    return FileResponse(render_output_image_dir / f"{file_uuid}.png")