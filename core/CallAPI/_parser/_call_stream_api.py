# ==== 标准库 ==== #
from typing import (
    AsyncIterator
)

# ==== 第三方库 ==== #
import openai
from openai.types.chat import ChatCompletion
from environs import Env
from loguru import logger

# ==== 自定义库 ==== #
from .._object import (
    Request,
    Delta,
)
from .._utils import (
    remove_keys_from_dicts,
    sum_string_lengths
)
from ._translation_chunk import translation_chunk
from ._call_api_base import CallStreamAPIBase
from .._exceptions import *

class StreamAPI(CallStreamAPIBase):
    async def call(self, user_id: str, request: Request) -> AsyncIterator[Delta]:
        """
        调用流式API

        :param user_id: 用户ID
        :param request: 请求对象
        :return: 响应流
        """
        try:
            # 创建OpenAI Client
            logger.info(f"Created OpenAI Client", user_id = user_id)
            client = openai.AsyncOpenAI(base_url=request.url, api_key=request.key)

            # 如果context为空，则抛出异常
            if not request.context:
                raise ValueError("context is required")
            
            # 请求流式连接
            logger.info(f"Start Connecting to the API", user_id = user_id)
            response: ChatCompletion = await client.chat.completions.create(
                model = request.model,
                temperature = request.temperature,
                top_p = request.top_p,
                frequency_penalty = request.frequency_penalty,
                presence_penalty = request.presence_penalty,
                max_tokens = request.max_tokens,
                max_completion_tokens=request.max_completion_tokens,
                stop = request.stop,
                stream = True,
                messages = remove_keys_from_dicts(request.context.full_context, {"reasoning_content"}) if not request.context.last_content.prefix else request.context.full_context,
                tools = request.function_calling.tools if request.function_calling else None,
            )
            async for chunk in response:
                # 翻译chunk
                delta_data = await translation_chunk(chunk)
                yield delta_data
        except openai.APITimeoutError as e:
            raise APITimeoutError(e)
        except openai.BadRequestError as e:
            raise BadRequestError(e)
        except openai.InternalServerError as e:
            raise APIServerError(e)
        except openai.APIConnectionError as e:
            raise APIConnectionError(e)
        except Exception as e:
            raise CallApiException(e) from e