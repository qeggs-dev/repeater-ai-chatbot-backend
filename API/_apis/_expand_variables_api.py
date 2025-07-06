from .._resource import chat, app
from fastapi import Form
from fastapi.responses import PlainTextResponse
from loguru import logger

@app.post("/userdata/variable/expand/{user_id}")
async def expand_variables(user_id: str, username: str | None = Form(None), text: str = Form(...)):
    """
    Endpoint for expanding variables
    """
    # 获取用户配置
    config = await chat.user_config_manager.load(user_id=user_id)

    if username is None:
        username = user_id
    
    # 调用PromptVP类处理文本
    prompt_vp = await chat.get_prompt_vp(
        user_id = user_id,
        user_name = username,
        model_type = "nomodel",
        config = config
    )
    output = prompt_vp.process(text)

    # 日志输出命中信息
    logger.info(f"Prompt Hits Variable: {prompt_vp.hit_var()}/{prompt_vp.discover_var()}({prompt_vp.hit_var() / prompt_vp.discover_var() if prompt_vp.discover_var() != 0 else 0:.2%})", user_id = user_id)

    # 返回结果
    return PlainTextResponse(output)