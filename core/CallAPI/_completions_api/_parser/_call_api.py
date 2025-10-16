# ==== 标准库 ==== #
import sys
import asyncio
import inspect
from typing import (
    Any,
    Awaitable,
    Callable,
    TextIO,
)
from datetime import datetime, timezone

# ==== 第三方库 ==== #
import openai
from openai.types.chat import ChatCompletion
from environs import Env
from loguru import logger

# ==== 自定义库 ==== #
from .._object import (
    Request,
    Response,
    Top_Logprob,
    Logprob,
    Delta,
    TokensCount
)
from ....Context import (
    FunctionResponseUnit,
    ContextObject,
    ContentUnit,
    ContextRole
)
from ....CallLog import CallLog, TimeStamp
from ....CoroutinePool import CoroutinePool
from TimeParser import (
    format_deltatime,
    format_deltatime_ns
)
from .._utils import (
    remove_keys_from_dicts,
    sum_string_lengths
)
from ._call_api_base import CallNstreamAPIBase
from .._exceptions import *

class CallAPI(CallNstreamAPIBase):
    async def call(self, user_id:str, request: Request) -> Response:
        """
        调用API

        :param user_id: 用户ID
        :param request: 请求对象
        :return: 响应对象
        """
        try:
            return await self._call(user_id, request)
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

    async def _call(self, user_id:str, request: Request) -> Response:
        """调用API"""
        # 创建模型响应对象
        model_response = Response()
        # 创建调用日志对象
        model_response.calling_log = CallLog()

        # 创建OpenAI Client
        logger.info(f"Created OpenAI Client", user_id = user_id)
        client = openai.AsyncOpenAI(base_url=request.url, api_key=request.key)

        # 写入调用日志基础数据
        model_response.calling_log.url = request.url
        model_response.calling_log.user_id = user_id
        model_response.calling_log.user_name = request.user_name
        model_response.calling_log.model = request.model
        model_response.calling_log.stream = request.stream

        # 如果上下文为空，则抛出异常
        if not request.context:
            raise ValueError("context is required")
        
        # 发送请求
        logger.info(f"Send Request", user_id = user_id)
        request_start_time = TimeStamp()
        response: ChatCompletion = await client.chat.completions.create(
            model = request.model,
            temperature = request.temperature,
            top_p = request.top_p,
            frequency_penalty = request.frequency_penalty,
            presence_penalty = request.presence_penalty,
            max_tokens = request.max_tokens,
            max_completion_tokens=request.max_completion_tokens,
            stop = request.stop,
            stream = False,
            messages = remove_keys_from_dicts(request.context.full_context, {"reasoning_content"}) if not request.context.last_content.prefix else request.context.full_context,
            tools = request.function_calling.tools if request.function_calling else None,
        )
        request_end_time = TimeStamp()

        # 创建响应内容单元
        model_response_content_unit:ContentUnit = ContentUnit()
        # 设置角色
        model_response_content_unit.role = ContextRole.ASSISTANT
        # chunk计数
        chunk_count:int = 0
        # 空chunk计数
        empty_chunk_count:int = 0
        self._print_file.write("\n")
        self._print_file.flush()

        # 处理响应基础信息
        if hasattr(response, "id"):
            model_response.id = response.id
        
        # 写入响应创建时间
        if hasattr(response, "created"):
            model_response.created = response.created
        
        # 写入模型名称
        if hasattr(response, "model"):
            model_response.model = response.model
        
        # 写入系统指纹
        if hasattr(response, "system_fingerprint"):
            model_response.system_fingerprint = response.system_fingerprint
        
        # 处理响应内容
        if hasattr(response, "choices"):
            choices = response.choices[0]
            # 写入完成原因
            if hasattr(choices, "finish_reason"):
                model_response.finish_reason = choices.finish_reason
            # 
            if hasattr(choices, "message"):
                # 处理输出内容
                if hasattr(choices.message, "content"):
                    model_response_content_unit.content = choices.message.content
                    self._print_file.write(f"\n\n{model_response_content_unit.content}\n\n")
                    self._print_file.flush()
                
                # 处理推理内容
                if hasattr(choices.message, "reasoning_content"):
                    model_response_content_unit.reasoning_content = choices.message.reasoning_content
                    self._print_file.write(f"\n\n\033[7m{model_response_content_unit.reasoning_content}\033[0m")
                    self._print_file.flush()
                
                # 处理工具调用
                if hasattr(choices.message, "tool_calls") and choices.message.tool_calls is not None:
                    for tool_call in choices.message.tool_calls:
                        # 处理调用函数
                        if hasattr(tool_call, "id"):
                            id = tool_call.id
                        else:
                            id = ""
                        if hasattr(tool_call, "type"):
                            type = tool_call.type
                        else:
                            type = ""
                        if hasattr(tool_call, "function"):
                            if hasattr(tool_call.function, "name"):
                                name = tool_call.function.name
                            else:
                                name = ""
                            if hasattr(tool_call.function, "arguments"):
                                arguments = tool_call.function.arguments
                            else:
                                arguments = ""
                        
                        # 添加调用函数信息
                        model_response_content_unit.funcResponse.callingFunctionResponse.append(
                            FunctionResponseUnit(
                                id = id,
                                type = type,
                                name = name,
                                arguments = arguments
                            )
                        )
        
        # 处理logprobs
        if hasattr(response.choices, "logprobs"):
            if hasattr(response.choices.logprobs, "content"):
                logprobs = []
                for token in response.choices.logprobs.content:
                    logprob = Logprob()
                    if hasattr(token, "token"):
                        logprob.token = token.token
                    if hasattr(token, "logprob"):
                        logprob.logprob = token.logprob
                    if hasattr(token, "top_logprob"):
                        top_logprobs = []
                        for top_token in token.top_logprob:
                            top_logprob = Top_Logprob()
                            if hasattr(top_token, "token"):
                                top_logprob.token = top_token.token
                            if hasattr(top_token, "logprob"):
                                top_logprob.logprob = top_token.logprob
                            top_logprobs.append(top_logprob)
                        logprob.top_logprobs = top_logprobs
                    logprobs.append(logprob)
                logprobs = logprobs
        
        # 处理usage数据
        model_response.token_usage = TokensCount()
        if hasattr(response, 'usage') and response.usage is not None:
            if hasattr(response.usage, 'prompt_tokens') and response.usage.prompt_tokens is not None:
                model_response.token_usage.prompt_tokens = response.usage.prompt_tokens
            if hasattr(response.usage, 'completion_tokens') and response.usage.completion_tokens is not None:
                model_response.token_usage.completion_tokens = response.usage.completion_tokens
            if hasattr(response.usage, 'total_tokens') and response.usage.total_tokens is not None:
                model_response.token_usage.total_tokens = response.usage.total_tokens
            if hasattr(response.usage, 'prompt_cache_hit_tokens') and response.usage.prompt_cache_hit_tokens is not None:
                model_response.token_usage.prompt_cache_hit_tokens = response.usage.prompt_cache_hit_tokens
            if hasattr(response.usage, 'prompt_cache_miss_tokens') and response.usage.prompt_cache_miss_tokens is not None:
                model_response.token_usage.prompt_cache_miss_tokens = response.usage.prompt_cache_miss_tokens

        self._print_file.write("\n\n")

        # 添加日志统计数据
        model_response.calling_log.id = model_response.id
        model_response.calling_log.total_chunk = chunk_count
        model_response.calling_log.empty_chunk = empty_chunk_count
        model_response.calling_log.request_start_time = request_start_time
        model_response.calling_log.request_end_time = request_end_time
        model_response.calling_log.total_tokens = model_response.token_usage.total_tokens
        model_response.calling_log.prompt_tokens = model_response.token_usage.prompt_tokens
        model_response.calling_log.completion_tokens = model_response.token_usage.completion_tokens
        model_response.calling_log.cache_hit_count = model_response.token_usage.prompt_cache_hit_tokens
        model_response.calling_log.cache_miss_count = model_response.token_usage.prompt_cache_miss_tokens

        # 添加上下文
        model_response.context = request.context
        model_response.context.context_list.append(model_response_content_unit)

        return model_response