from .._resource import (
    chat,
    app,
    core
)
from fastapi import Form
from fastapi.responses import (
    JSONResponse,
    PlainTextResponse
)
from fastapi import HTTPException
from loguru import logger

@app.get("/userdata/context/get/{user_id}")
async def get_context(user_id: str):
    """
    Endpoint for getting context
    """
    # 从chat.context_manager中加载用户ID为user_id的上下文
    context = await chat.context_manager.load(user_id, [])

    logger.info(f"Get Context", user_id = user_id)

    # 返回JSON格式的上下文
    return JSONResponse(context)

@app.get("/userdata/context/length/{user_id}")
async def get_context_length(user_id: str):
    """
    Endpoint for getting context
    """
    # 从chat.context_manager中加载用户ID为user_id的上下文
    context_loader = await chat.get_context_loader()
    context = await context_loader.get_context_object(user_id)
    # 将上下文转换为Context.ContextObject对象
    context = core.Context.ContextObject().from_context(context)
    
    logger.info(f"Get Context length", user_id = user_id)

    # 返回JSONResponse，包含上下文的总长度和上下文的长度
    return JSONResponse(
        {
            "total_context_length": context.total_length,
            "context_length": len(context)
        }
    )

@app.get("/userdata/context/userlist")
async def get_context_userlist():
    """
    Endpoint for getting context
    """
    # 从chat.context_manager中获取所有用户ID
    userid_list = await chat.context_manager.get_all_user_id()

    logger.info(f"Get Context userlist", user_id = "[System]")

    # 返回JSONResponse，包含所有用户ID
    return JSONResponse(userid_list)

@app.post("/userdata/context/withdraw/{user_id}")
async def withdraw_context(user_id: str, index: int = Form(...)):
    """
    Endpoint for withdrawing context
    """
    # 从context_loader中加载用户ID为user_id的上下文
    context_loader = await chat.get_context_loader()
    context = await context_loader.get_context_object(user_id)

    # 检查索引是否在上下文范围内
    if 0 <= index < len(context.context_list):
        context.context_list.pop(index)
        await context_loader.save(user_id, context)
    else:
        raise HTTPException(400, "Index out of range")
    
    logger.info(f"Withdraw a Last Context", user_id = user_id)
    
    # 返回JSONResponse，新的上下文内容
    return JSONResponse(context)

@app.post("/userdata/context/rewrite/{user_id}")
async def rewrite_context(user_id: str, index: int = Form(...), content: str = Form(""), reasoning_content: str = Form("")):
    """
    Endpoint for rewriting context
    """
    # 从context_loader中加载用户ID为user_id的上下文
    context_loader = await chat.get_context_loader()
    context = await context_loader.get_context_object(user_id)

    # 检查索引是否在上下文范围内
    if 0 <= index < len(context.context_list):
        if content:
            context.context_list[index].content = content
        if reasoning_content:
            if context.context_list[index].role == "assistant":
                context.context_list[index].reasoning_content = reasoning_content
            else:
                raise HTTPException(400, "Only assistant can have reasoning_content")
        await context_loader.save(user_id, context)
    else:
        raise HTTPException(400, "Index out of range")
    
    logger.info(f"Rewrite {index} Context", user_id = user_id)
    
    # 返回JSONResponse，新的上下文内容
    return JSONResponse(context)

@app.get("/userdata/context/branch/{user_id}")
async def get_context_branch_id(user_id: str):
    """
    Endpoint for getting context branch id list
    """
    # 获取用户ID为user_id的上下文分支ID
    branchs = await chat.context_manager.get_all_item_id(user_id)

    logger.info(f"Get Context branch id list", user_id = user_id)

    # 返回上下文分支ID
    return JSONResponse(branchs)

@app.get("/userdata/context/now_branch/{user_id}")
async def get_context_now_branch_id(user_id: str):
    """
    Endpoint for getting context branch id
    """
    # 获取用户ID为user_id的上下文分支ID
    branch_id = await chat.context_manager.get_default_item_id(user_id)

    logger.info(f"Get Context branch id", user_id = user_id)

    # 返回上下文分支ID
    return PlainTextResponse(branch_id)

@app.post("/userdata/context/change/{user_id}")
async def change_context(user_id: str, new_branch_id: str):
    """
    Endpoint for changing context
    """

    # 设置用户ID为user_id的上下文为new_context_id
    await chat.context_manager.set_default_item_id(user_id, item = new_branch_id)

    logger.info("Change Context to {new_branch_id}", user_id = user_id, new_branch_id = new_branch_id)

    # 返回成功文本
    return PlainTextResponse("Context changed successfully")

@app.delete("/userdata/context/delete/{user_id}")
async def delete_context(user_id: str):
    """
    Endpoint for deleting context
    """
    # 删除用户ID为user_id的上下文
    await chat.context_manager.delete(user_id)

    logger.info("Delete Context", user_id = user_id)

    # 返回成功文本
    return PlainTextResponse("Context deleted successfully")