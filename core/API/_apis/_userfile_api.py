from .._resource import (
    app,
    chat
)
from ...Context_Manager import (
    ContextObject
)
from fastapi import (
    HTTPException
)
from fastapi.responses import (
    StreamingResponse
)
from loguru import logger
from io import BytesIO
import zipfile
import yaml
import orjson


@app.get("/userdata/file/{user_id}.zip")
async def get_userdata_file(user_id: str):
    """
    Endpoint for getting userdata file

    Args:
        user_id (str): User ID

    Returns:
        StreamingResponse: File stream
    """
    # 创建虚拟文件缓冲区
    buffer = BytesIO()
    context_loader = await chat.get_context_loader()
    context = await context_loader.get_context_object(user_id = user_id)
    config = await chat.user_config_manager.load(user_id = user_id)
    prompt = await chat.prompt_manager.load(user_id = user_id, default = "")

    def readable_context(context: ContextObject) -> str:
        text = "======== Context  ========\n"
        for item in context.context_list:
            text += f"[{item.role}]: \n{item.content}\n\n"
            text += "==========================\n\n"
        return text
            

    # 创建zip文件并写入
    with zipfile.ZipFile(buffer, "w") as zipf:
        zipf.writestr("user_context.json", orjson.dumps(context.context))
        zipf.writestr("user_context_readable.txt", readable_context(context))
        zipf.writestr("user_prompt.json", orjson.dumps(prompt))
        zipf.writestr("user_prompt_readable.txt", prompt)
        zipf.writestr("user_config.json", orjson.dumps(config.configs))
        zipf.writestr("user_config_readable.yaml", (yaml.dump(config.configs, indent = 2, allow_unicode = True) if config.configs else ""))
    buffer.seek(0)

    logger.info(f"downloaded userdata file", user_id = user_id)

    # 返回zip文件
    return StreamingResponse(buffer, media_type = "application/zip")