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

class ChatRequest(BaseModel):
    message: str = ""
    user_name: str = ""
    role: str = "user"
    role_name: str | None = None
    model_type: str | None = None
    load_prompt: bool = True
    save_context: bool = True
    reference_context_id: str | None = None
    continue_completion: bool = False


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
            user_name = request.user_name,
            role = request.role,
            role_name = request.role_name,
            model_type = request.model_type,
            print_chunk = True,
            load_prompt = request.load_prompt,
            save_context = request.save_context,
            reference_context_id = request.reference_context_id,
            continue_completion = request.continue_completion
        )
    except core.ApiInfo.APIGroupNotFoundError as e:
        raise HTTPException(detail=str(e), status_code=400)
    return JSONResponse(context)