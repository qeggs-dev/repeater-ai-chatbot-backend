# ==== 标准库 ==== #
from typing import (
    Any,
    Awaitable,
    AsyncIterator,
    Callable
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

class ClientNoStream(ClientBase):
    """Client without stream"""
    
    async def submit_Request(self, user_id:str, request: Request) -> Response:
        """提交请求，并等待API返回结果"""
        try:
            response = await self._submit_task(user_id, request)
            if not isinstance(response, Response):
                generator = StreamingResponseGenerationLayer(user_id, request, response)
                for chunk in generator:
                    pass
                output = generator.response
            else:
                output = response

        except openai.NotFoundError:
            raise ModelNotFoundError(request.model)
        except openai.APIConnectionError:
            raise APIConnectionError(f"{request.url} Connection Failed")
        
        return output
    
    async def _submit_task(self, user_id: str, request: Request) -> AsyncIterator[Delta] | Response:
        if request.stream:
            client = StreamAPI()
            call = client.call(
                user_id = user_id,
                request = request
            )
        else:
            client = CallAPI()
            call = await client.call(
                user_id = user_id,
                request = request
            )
        return call