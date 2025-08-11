# ==== 标准库 ==== #
from typing import (
    Any,
    Awaitable,
    AsyncIterator,
    Callable,
)

# ==== 第三方库 ==== #
import openai

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
    
    async def submit_Request(self, user_id:str, request: Request) -> AsyncIterator[Delta]:
        """提交请求，并等待API返回结果"""
        try:
            return await self._submit_task(user_id, request)
        except openai.NotFoundError:
            raise ModelNotFoundError(request.model)
        except openai.APIConnectionError:
            raise APIConnectionError(f"{request.url} Connection Failed")
    
    async def _submit_task(self, user_id: str, request: Request) -> AsyncIterator[Delta]:
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
    