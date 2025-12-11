from typing import AsyncIterator
import orjson
from environs import Env
env = Env()
env.read_env()
from fastapi.responses import (
    ORJSONResponse,
    StreamingResponse
)
from fastapi.exceptions import (
    HTTPException
)
from ..._resource import app, chat
from ....Core_Response import Response
from ....ApiInfo import APIGroupNotFoundError
from ....CallAPI import CompletionsAPI

import orjson

from ._requests import (
    ChatRequest
)

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
            user_info = request.user_info,
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
            return ORJSONResponse(
                context.model_dump(
                    exclude_defaults = True
                ),
                status_code=200
            )
        else:
            async def generator_wrapper(context: AsyncIterator[CompletionsAPI.Delta]) -> AsyncIterator[bytes]:
                async for chunk in context:
                    yield orjson.dumps(chunk.as_dict) + b"\n"

            return StreamingResponse(generator_wrapper(context), media_type="application/x-ndjson")
    except APIGroupNotFoundError as e:
        raise HTTPException(detail=str(e), status_code=404)