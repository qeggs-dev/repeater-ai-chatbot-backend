# ==== 标准库 ==== #
from typing import (
    Any,
    Awaitable,
    AsyncIterator,
    Callable
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

class ClientNoStream(ClientBase):
    """Client without stream"""
    
    async def submit_Request(self, user_id:str, request: Request) -> Response:
        """提交请求，并等待API返回结果"""
        try:
            response = await self._submit_task(user_id, request)
            if not isinstance(response, Response):
                generator = StreamingResponseGenerationLayer(user_id, request, response)
                async for chunk in generator:
                    pass
                output = generator.response
            else:
                output = response

            await self._preprocess_response(user_id, request, output)

        except openai.NotFoundError:
            raise ModelNotFoundError(request.model)
        except openai.APIConnectionError:
            raise APIConnectionError(f"{request.url} Connection Failed")
        
        return output
    
    async def _submit_task(self, user_id: str, request: Request) -> AsyncIterator[Delta] | Response:
        try:
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