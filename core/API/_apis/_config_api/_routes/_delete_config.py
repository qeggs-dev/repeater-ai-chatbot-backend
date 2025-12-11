from ...._resource import (
    chat,
    app
)
from typing import Any
from fastapi.responses import (
    ORJSONResponse,
    PlainTextResponse
)
from .....User_Config_Manager import (
    UserConfigs
)
from .._requests import (
    SetConfigRequest
)
from fastapi import (
    HTTPException
)
from fastapi import (
    Form
)
from loguru import logger

from pydantic import BaseModel, ValidationError

@app.put("/userdata/config/delkey/{user_id}")
async def delete_config_field(user_id: str, key: str = Form(...)):
    """
    Endpoint for delkey config

    Parameters:
        user_id (str): User ID
        key (str): User config key

    Returns:
        ORJSONResponse: New config content
    """

    # 读取配置
    config = await chat.user_config_manager.load(user_id=user_id)
    
    # 更新配置
    try:
        if key in type(config).model_fields.keys():
            setattr(
                config,
                key,
                type(config).model_fields[key].default
            )
        else:
            raise HTTPException(400, "Invalid config key")
    except ValidationError as e:
        raise HTTPException(500, "The default value is not one of the valid values for this field and can not be assigned.")

    # 保存配置
    await chat.user_config_manager.save(user_id=user_id, configs=config)

    logger.info("Delete user config field: {key}", user_id = user_id, key = key)

    # 返回新配置内容
    return ORJSONResponse(config.model_dump(exclude_defaults=True))

@app.delete("/userdata/config/delete/{user_id}")
async def delete_config(user_id: str):
    """
    Endpoint for deleting config

    Args:
        user_id (str): The user id

    Returns:
        PlainTextResponse: Plain text response
    """
    # 删除配置
    await chat.user_config_manager.delete(user_id)

    logger.info("Delete user config", user_id = user_id)

    # 返回成功文本
    return PlainTextResponse("Config deleted successfully")