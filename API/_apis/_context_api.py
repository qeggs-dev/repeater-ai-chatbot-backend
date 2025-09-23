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
from pydantic import BaseModel
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

    logger.info(f"Get Context userlist")

    # 返回JSONResponse，包含所有用户ID
    return JSONResponse(userid_list)

@app.post("/userdata/context/withdraw/{user_id}")
async def withdraw_context(user_id: str, length: int | None = Form(None, ge=0)):
    """
    Endpoint for withdrawing context
    """
    # 从context_loader中加载用户ID为user_id的上下文
    context_loader = await chat.get_context_loader()
    context = await context_loader.get_context_object(user_id)

    if length is None:
        pop_items: list[core.Context.ContentUnit] = []
        
        # 安全检查
        if not context.context_list:
            return JSONResponse(
                {
                    "status": "success",
                    "deleted": 0,
                    "context": context.context
                }
            )
        
        # 第一步：pop直到找到助手消息
        while (context.context_list and 
            context.last_content.role != core.Context.ContextRole.ASSISTANT):
            pop_items.append(context.pop())
        
        # 第二步：pop助手消息
        while (context.context_list and 
            context.last_content.role == core.Context.ContextRole.ASSISTANT):
            pop_items.append(context.pop())
        
        # 第三步：pop相关联的用户消息
        while (context.context_list and 
            context.last_content.role != core.Context.ContextRole.ASSISTANT):
            pop_items.append(context.pop())
        logger.info(f"Withdraw a Last {len(pop_items)} Contexts")
        
    else:
        # 检查索引是否在上下文范围内
        if 0 <= length < len(context.context_list):
            pop_items = context.pop_last_n(length)
        else:
            raise HTTPException(400, "Index out of range")
        
        logger.info(f"Withdraw a Last {length} Context", user_id = user_id)
    
    # 返回JSONResponse，新的上下文内容
    await context_loader.save(user_id, context)
    return JSONResponse(
        {
            "status": "success",
            "deleted": len(pop_items),
            "context": context.context
        }
    )

class RewriteContext(BaseModel):
    index: int
    content: str | None = None
    reasoning_content: str | None = None

@app.post("/userdata/context/rewrite/{user_id}")
async def rewrite_context(user_id: str, rewrite_context: RewriteContext):
    """
    Endpoint for rewriting context
    """
    # 从context_loader中加载用户ID为user_id的上下文
    context_loader = await chat.get_context_loader()
    context = await context_loader.get_context_object(user_id)

    # 检查索引是否在上下文范围内
    if 0 <= rewrite_context.index < len(context.context_list):
        if rewrite_context.content:
            context.context_list[rewrite_context.index].content = rewrite_context.content
        if rewrite_context.reasoning_content:
            if context.context_list[rewrite_context.index].role == "assistant":
                context.context_list[rewrite_context.index].reasoning_content = rewrite_context.reasoning_content
            else:
                raise HTTPException(400, "Only assistant can have reasoning_content")
        await context_loader.save(user_id, context)
    else:
        raise HTTPException(400, "Index out of range")
    
    logger.info(f"Rewrite {rewrite_context.index} Context", user_id = user_id)
    
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