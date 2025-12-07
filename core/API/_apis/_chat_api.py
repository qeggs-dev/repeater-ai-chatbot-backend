from typing import AsyncIterator, Any
import orjson
from environs import Env
env = Env()
env.read_env()
from fastapi.responses import (
    FileResponse,
    ORJSONResponse,
    PlainTextResponse,
    StreamingResponse
)
from fastapi.exceptions import (
    HTTPException
)
from .._resource import app, chat
from ...Core_Response import Response
from ...Request_User_Info import Request_User_Info
from ...ApiInfo import APIGroupNotFoundError
from ...CallAPI import CompletionsAPI
from ...Context_Manager import ContextRole
from pydantic import BaseModel, Field
import orjson

class UserInfo(BaseModel):
    username: str | None = None
    nickname: str | None = None
    age: int | None = None
    gender: str | None = None

class ChatRequest(BaseModel):
    message: str = ""
    user_info: UserInfo = Field(default_factory=UserInfo)
    role: ContextRole = ContextRole.USER
    role_name: str | None = None
    model_uid: str | None = None
    load_prompt: bool | None = None
    save_context: bool | None = None
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
        context = await chat.chat(
            user_id = user_id,
            message = request.message,
            user_info = (
                Request_User_Info(
                    username = request.user_info.username,
                    nickname = request.user_info.nickname,
                    age = request.user_info.age,
                    gender = request.user_info.gender
                )
                if request.user_info else None
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
        if isinstance(context, Response):
            return ORJSONResponse(context.as_dict, status_code=200)
        else:
            async def generator_wrapper(context: AsyncIterator[CompletionsAPI.Delta]) -> AsyncIterator[bytes]:
                async for chunk in context:
                    yield orjson.dumps(chunk.as_dict) + b"\n"

            return StreamingResponse(generator_wrapper(context), media_type="application/x-ndjson")
    except APIGroupNotFoundError as e:
        raise HTTPException(detail=str(e), status_code=404)