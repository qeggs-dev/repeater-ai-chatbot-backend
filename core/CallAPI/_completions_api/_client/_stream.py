# ==== 标准库 ==== #
from typing import (
    Any,
    Awaitable,
    AsyncIterator,
    Callable,
)

# ==== 第三方库 ==== #
import openai
from loguru import logger

# ==== 自定义库 ==== #
from .._object import (
    Request,
    Response,
    Delta
)
from .._parser import (
    CallAPI,
    StreamAPI
)
from .._exceptions import *
from .._parser import StreamingResponseGenerationLayer
from ._client import ClientBase

class ClientStream(ClientBase):
    """Client with stream"""
    
    async def submit_Request(self, user_id:str, request: Request, response_callback: Callable[[Response], Awaitable[None]] | None = None) -> AsyncIterator[Delta]:
        """提交请求，并等待API返回结果"""
        try:
            generator = self._submit_task(user_id, request)
            async def stream() -> AsyncIterator[Delta]:
                warping_generator = StreamingResponseGenerationLayer(user_id, request, generator)
                async for delta in warping_generator:
                    yield delta
                await self._preprocess_response(user_id, request, warping_generator.response)
                if response_callback is not None:
                    await response_callback(warping_generator.response)
            
            return stream()
                
        except openai.NotFoundError:
            raise ModelNotFoundError(request.model)
        except openai.APIConnectionError:
            raise APIConnectionError(f"{request.url} Connection Failed")
    
    async def _submit_task(self, user_id: str, request: Request) -> AsyncIterator[Delta]:
        try:
            if request.stream:
                client = StreamAPI()
            else:
                raise StreamNotAvailable("When request.stream == True, the stream is not available.")
            generator = client.call(
                user_id = user_id,
                request = request
            )

            async for delta in generator:
                yield delta
        except openai.BadRequestError as e:
            if e.code in range(400, 500):
                logger.error(f"BadRequestError: {e}", user_id = user_id)
                raise BadRequestError(e.message)
            elif e.code in range(500, 600):
                logger.error(f"API Server Error: {e}", user_id = user_id)
                raise APIServerError(e.message)
        except Exception as e:
            logger.error(f"Error: {e}", user_id = user_id)
            raise CallApiException(e)