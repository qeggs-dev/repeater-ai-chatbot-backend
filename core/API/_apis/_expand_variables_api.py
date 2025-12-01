from .._resource import chat, app
from ...Request_User_Info import Request_User_Info
from fastapi import Form
from fastapi.responses import PlainTextResponse
from loguru import logger
from pydantic import BaseModel

class ExpandRequest(BaseModel):
    user_name: str | None = None
    user_nickname: str | None = None
    user_age: int | None = None
    user_sex: str | None = None
    text: str

@app.post("/userdata/variable/expand/{user_id}")
async def expand_variables(user_id: str, request: ExpandRequest):
    """
    Endpoint for expanding variables
    """
    # 获取用户配置
    config = await chat.user_config_manager.load(user_id=user_id)

    if request.user_name is None:
        user_name = user_id
    else:
        user_name = request.user_name
    
    # 调用PromptVP类处理文本
    prompt_vp = await chat.get_prompt_vp(
        user_id = user_id,
        user_info = Request_User_Info(
            username = user_name,
            nickname = request.user_nickname,
            age = request.user_age,
            gender = request.user_sex
        ),
        model_uid = "nomodel",
        config = config
    )
    output = prompt_vp.process(request.text)

    # 日志输出命中信息
    logger.info(f"Prompt Hits Variable: {prompt_vp.hit_var()}/{prompt_vp.discover_var()}({prompt_vp.hit_var() / prompt_vp.discover_var() if prompt_vp.discover_var() != 0 else 0:.2%})", user_id = user_id)

    # 返回结果
    return PlainTextResponse(output)