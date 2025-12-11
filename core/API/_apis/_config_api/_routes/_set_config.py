from ...._resource import (
    chat,
    app
)
from fastapi.responses import (
    ORJSONResponse,
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
from loguru import logger

from pydantic import ValidationError

@app.put("/userdata/config/set/{user_id}")
async def set_config(user_id: str, request: UserConfigs):
    await chat.user_config_manager.force_write(user_id=user_id, configs=request)
    logger.info(
        "Set user config: \n{config}",
        user_id = user_id,
        config = request.model_dump_json(indent=4, ensure_ascii=False, exclude_defaults=True)
    )
    return ORJSONResponse(
        request.model_dump(exclude_defaults=True)
    )

@app.put("/userdata/config/set/{user_id}/{key}")
async def set_config_field(user_id: str, key: str, request: SetConfigRequest):
    """
    Endpoint for setting config

    Args:
        user_id (str): User ID
        key (str): Config Key
        request (SetConfigRequest): Config Value
    
    Returns:
        ORJSONResponse: Config
    """
    # 允许的值类型
    TYPES = {
        "int": int,
        "float": float,
        "string": str,
        "bool": bool,
        "dict": dict,
        "list": list,
        "null": None
    }
    # 检查值类型是否有效
    if request.type not in TYPES:
        raise HTTPException(400, "Invalid value type")
    if request.type == "null":
        value = None
    else:
        # 将值转换为指定类型
        value = TYPES[request.type](request.value)
    
    # 读取配置
    config = await chat.user_config_manager.load(user_id=user_id)
    
    # 更新配置
    if key in type(config).model_fields.keys():
        try:
            setattr(config, key, value)
        except ValidationError as e:
            errors = e.errors()
            text_buffer:list[str] = []
            for error in errors:
                text_buffer.append(f"{'.'.join(error['loc'])}: {error['msg']}")
            raise HTTPException(400, "\n".join(text_buffer))
    else:
        raise HTTPException(400, "Invalid config key")

    # 保存配置
    # await chat.user_config_manager.save(user_id=user_id, configs=config)
    await chat.user_config_manager.force_write(user_id=user_id, configs=config)
    
    logger.info(
        "Set user config {key}={value}(type:{value_type})",
        user_id = user_id,
        key = key,
        value = value,
        value_type = request.type
    )

    # 返回新配置内容
    return ORJSONResponse(
        config.model_dump(exclude_defaults=True),
    )