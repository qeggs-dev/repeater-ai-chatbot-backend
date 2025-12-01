from .._resource import (
    chat,
    app
)
from typing import Any
from fastapi.responses import (
    JSONResponse,
    PlainTextResponse
)
from fastapi import (
    HTTPException
)
from fastapi import (
    Form
)
from loguru import logger

@app.get("/userdata/config/get/{user_id}")
async def change_config(user_id: str):
    """
    Endpoint for changing config
    """
    # 获取用户ID为user_id的配置
    config = await chat.get_config(user_id = user_id)
    
    logger.info(f"Get user config", user_id = user_id)

    # 返回配置
    return JSONResponse(config.configs)

@app.put("/userdata/config/set/{user_id}/{value_type}")
async def set_config(user_id: str, value_type: str, key: str = Form(...), value: Any = Form(...)):
    """
    Endpoint for setting config

    Args:
        user_id (str): User ID
        value_type (str): Value Type(Automatic type conversion)
        key (str): Config Key
        value (Any): Config Value
    
    Returns:
        JSONResponse: Config
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
    if value_type not in TYPES:
        raise HTTPException(400, "Invalid value type")
    if value_type == "null":
        value = None
    else:
        # 将值转换为指定类型
        value = TYPES[value_type](value)
    
    # 读取配置
    config = await chat.user_config_manager.load(user_id=user_id)
    
    # 更新配置
    config[key] = value

    # 保存配置
    # await chat.user_config_manager.save(user_id=user_id, configs=config)
    await chat.user_config_manager.force_write(user_id=user_id, configs=config)
    
    logger.info("Set user config {key}={value}(type:{value_type})", user_id = user_id, key = key, value = value, value_type = value_type)

    # 返回新配置内容
    return JSONResponse(config.configs)

@app.put("/userdata/config/delkey/{user_id}")
async def delkey_config(user_id: str, key: str = Form(...)):
    """
    Endpoint for delkey config

    Parameters:
        user_id (str): User ID
        key (str): User config key

    Returns:
        JSONResponse: New config content
    """

    # 读取配置
    config = await chat.user_config_manager.load(user_id=user_id)
    
    # 如果项不存在，则抛出错误
    if key not in config:
        raise HTTPException(400, "Key not found")

    # 删除项
    del config[key]

    # 保存配置
    await chat.user_config_manager.save(user_id=user_id, configs=config)

    logger.info("Del user config {key}", user_id = user_id, key = key)

    # 返回新配置内容
    return JSONResponse(config)

@app.get("/userdata/config/userlist")
async def get_config_userlist():
    """
    Endpoint for getting config userlist

    Returns:
        JSONResponse: A JSON response containing the list of user IDs
    """

    # 获取所有用户ID
    userid_list = await chat.user_config_manager.get_all_user_id()

    logger.info(f"Get user config userlist")

    # 返回用户ID列表
    return JSONResponse(userid_list)

@app.get("/userdata/config/branchs/{user_id}")
async def get_config_branch_id(user_id: str):
    """
    Endpoint for get config branch id

    Args:
        user_id (str): The user id
    
    Returns:
        JSONResponse: Current user's branch list
    """

    # 获取平行配置路由ID列表
    branchs = await chat.user_config_manager.get_all_item_id(user_id)

    logger.info(f"Get user branchs list", user_id = user_id)

    # 返回分支ID列表
    return JSONResponse(branchs)

@app.get("/userdata/config/now_branch/{user_id}")
async def get_config_now_branch_id(user_id: str):
    """
    Endpoint for get config branch id

    Args:
        user_id (str): User id

    Returns:
        JSONResponse: Now Branch id
    """

    # 获取当前配置路由ID
    branch_id = await chat.user_config_manager.get_default_item(user_id)

    logger.info(f"Get user now branch id", user_id = user_id)

    # 返回分支ID
    return PlainTextResponse(branch_id)

@app.put("/userdata/config/change/{user_id}")
async def change_config(user_id: str, new_branch_id: str = Form(...)):
    """
    Endpoint for changing config

    Args:
        user_id (str): User id
        new_branch_id (str): New branch id
    
    Returns:
        PlainTextResponse: Plain text response
    """

    # 设置平行配置路由
    await chat.user_config_manager.set_default_item(user_id, item = new_branch_id)

    logger.info("Change user config branch id to {new_branch_id}", user_id = user_id, new_branch_id = new_branch_id)

    # 返回成功文本
    return PlainTextResponse("Config changed successfully")


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