from .._resource import (
    chat,
    app
)
from fastapi import Form
from fastapi.responses import (
    JSONResponse,
    PlainTextResponse
)
from loguru import logger

@app.get("/userdata/prompt/get/{user_id}")
async def get_prompt(user_id: str):
    """
    Endpoint for setting prompt

    Args:
        user_id (str): User ID
    
    Returns:
        PlainTextResponse: User's prompt
    """
    # 获取用户ID为user_id的提示词
    prompt = await chat.prompt_manager.load(user_id)

    logger.info("Get prompt", user_id=user_id)

    # 返回提示词内容
    return PlainTextResponse(prompt)

@app.put("/userdata/prompt/set/{user_id}")
async def set_prompt(user_id: str, prompt: str = Form(...)):
    """
    Endpoint for setting prompt

    Args:
        user_id (str): User ID
        prompt (str): Prompt content

    Returns:
        PlainTextResponse: Success message
    """
    # 设置用户ID为user_id的提示词为prompt
    await chat.prompt_manager.save(user_id, prompt)

    logger.info("Set prompt", user_id=user_id)

    # 返回成功文本
    return PlainTextResponse("Prompt set successfully")

@app.get("/userdata/prompt/userlist")
async def get_prompt_userlist():
    """
    Endpoint for getting prompt user list

    Returns:
        JSONResponse: User ID list
    """
    # 获取所有用户ID
    userid_list = await chat.prompt_manager.get_all_user_id()

    logger.info("Get prompt user list")

    # 返回用户ID列表
    return JSONResponse(userid_list)

@app.get("/userdata/prompt/branchs/{user_id}")
async def get_prompt_branch_id(user_id: str):
    """
    Endpoint for getting prompt branch ID

    Args:
        user_id (str): User ID

    Returns:
        JSONResponse: Prompt branch ID
    """
    # 获取用户ID为user_id的提示词分支ID
    branchs = await chat.prompt_manager.get_all_item_id(user_id)

    logger.info("Get prompt branch", user_id=user_id)

    # 返回分支ID
    return JSONResponse(branchs)

@app.get("/userdata/prompt/now_branch/{user_id}")
async def get_prompt_now_branch_id(user_id: str):
    """
    Endpoint for getting prompt branch ID

    Args:
        user_id (str): User ID

    Returns:
        JSONResponse: Now Branch ID
    """
    # 获取用户ID为user_id的提示词分支ID
    branch_id = await chat.prompt_manager.get_default_item_id(user_id)

    logger.info("Get prompt branch", user_id=user_id)

    # 返回分支ID
    return PlainTextResponse(branch_id)

@app.put("/userdata/prompt/change/{user_id}")
async def change_prompt(user_id: str, new_branch_id: str = Form(...)):
    """
    Endpoint for changing prompt

    Args:
        user_id (str): User ID
        new_branch_id (str): New prompt ID
    
    Returns:
        PlainTextResponse: Success text for successful change
    """

    # 设置用户ID为user_id的提示词为new_prompt_id
    await chat.prompt_manager.set_default_item_id(user_id, item = new_branch_id)

    logger.info("Change prompt to {new_branch_id}", user_id=user_id, new_branch_id=new_branch_id)

    # 返回成功文本
    return PlainTextResponse("Prompt changed successfully")

@app.delete("/userdata/prompt/delete/{user_id}")
async def delete_prompt(user_id: str):
    """
    Endpoint for deleting prompt

    Args:
        user_id (str): User ID

    Returns:
        PlainTextResponse: Success text for successful deletion
    """
    # 删除用户ID为user_id的提示词
    await chat.prompt_manager.delete(user_id)

    logger.info("Delete prompt", user_id=user_id)

    # 返回成功文本
    return PlainTextResponse("Prompt deleted successfully")