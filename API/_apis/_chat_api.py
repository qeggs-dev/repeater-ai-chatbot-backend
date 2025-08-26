from typing import AsyncIterator, Any
import orjson
from environs import Env
env = Env()
env.read_env()
from fastapi import (
    FastAPI,
    Request,
    BackgroundTasks,
    Form,
    Query,
    Header
)
from fastapi.responses import (
    FileResponse,
    JSONResponse,
    PlainTextResponse,
    StreamingResponse
)
from fastapi.exceptions import (
    HTTPException
)
from loguru import logger
from .._resource import app, chat, core
from pydantic import BaseModel
import orjson

class UserInfo(BaseModel):
    username: str | None = None
    nickname: str | None = None
    age: int | None = None
    gender: str | None = None

class ChatRequest(BaseModel):
    message: str = ""
    user_info: UserInfo | None = None
    role: str = "user"
    role_name: str | None = None
    model_uid: str | None = None
    load_prompt: bool = True
    save_context: bool = True
    reference_context_id: str | None = None
    continue_completion: bool = False
    stream: bool = False

@app.post("/chat/completion/{user_id}")
async def chat_endpoint(
    user_id: str,
    request: ChatRequest
):
    """
    Endpoint for chat
    """
    if request.continue_completion and request.message:
        raise HTTPException(detail="Cannot send message when continuing completion", status_code=400)
    try:
        context = await chat.Chat(
            user_id = user_id,
            message = request.message,
            user_info = core.RequestUserInfo.UserInfo(
                username = request.user_info.username,
                nickname = request.user_info.nickname,
                age = request.user_info.age,
                gender = request.user_info.gender
            ),
            role = request.role,
            role_name = request.role_name,
            model_uid = request.model_uid,
            print_chunk = True,
            load_prompt = request.load_prompt,
            save_context = request.save_context,
            reference_context_id = request.reference_context_id,
            continue_completion = request.continue_completion,
            stream = request.stream
        )
        if not request.stream:
            return JSONResponse(context.as_dict)
        else:
            async def generator_wrapper(context: AsyncIterator[core.CallAPI.Delta]) -> AsyncIterator[bytes]:
                async for chunk in context:
                    yield orjson.dumps(chunk.as_dict) + b"\n"

            return StreamingResponse(generator_wrapper(context), media_type="application/x-ndjson")
    except core.ApiInfo.APIGroupNotFoundError as e:
        raise HTTPException(detail=str(e), status_code=400)