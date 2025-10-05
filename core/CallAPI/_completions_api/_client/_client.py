# ==== 标准库 ==== #
import asyncio
import inspect
from typing import (
    Any,
    Awaitable,
    AsyncIterator,
    Callable,
)
import time
from datetime import datetime, timezone
from abc import ABC, abstractmethod

# ==== 第三方库 ==== #
import openai
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
from ...Context import (
    FunctionResponseUnit,
    ContextObject,
    ContentUnit,
    ContextRole
)
from ...CallLog import CallLog
from ...CoroutinePool import CoroutinePool
from TimeParser import (
    format_deltatime,
    format_deltatime_ns
)
from .._parser import (
    CallAPI,
    StreamAPI
)
from .._exceptions import *
from .._utils import (
    remove_keys_from_dicts,
    sum_string_lengths
)
import math

class ClientBase(ABC):
    def __init__(self, max_concurrency: int = 1000):
        # 协程池
        self.coroutine_pool = CoroutinePool(max_concurrency)
    # region 协程池管理
    async def set_concurrency(self, new_max: int):
        """动态修改并发限制"""
        await self.coroutine_pool.set_concurrency(new_max)
    # endregion

    # region 提交任务
    @abstractmethod
    async def submit_Request(self, user_id:str, request: Request) -> Response:
        """提交请求，并等待API返回结果"""
        pass
    # endregion

    # region 预处理响应数据
    async def _preprocess_response(self, user_id: str, request: Request, response: Response):
        if response.context.last_content.reasoning_content:
            logger.bind(donot_send_console=True).info("Reasoning_Content: \n{reasoning_content}", reasoning_content = request.context.last_content.reasoning_content, user_id = user_id)
        if response.context.last_content.content:
            logger.bind(donot_send_console=True).info("Content: \n{content}", content = request.context.last_content.content, user_id = user_id)
        
        await self._print_log(
            user_id = user_id,
            request = request,
            response = response
        )
        return response
    # endregion

    # region 任务
    async def _submit_task(self, user_id: str, request: Request):
        if request.stream:
            client = StreamAPI()
        else:
            client = CallAPI()
        try:
            return await client.call(
                user_id = user_id,
                request = request
            ), client
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
    # endregion

    # region 打印日志
    async def _print_log(self, user_id: str, request: Request, response: Response):
        """
        打印统计日志

        :param user_id: 用户ID
        :param request: 请求对象
        :param response: 响应对象
        """
        logger.info("============= API INFO =============", user_id = user_id)
        logger.info(f"API_URL: {request.url}", user_id = user_id)
        logger.info(f"Model: {response.model}", user_id = user_id)
        logger.info(f"UserName: {request.user_name}", user_id = user_id)
        logger.info(f"Chat Completion ID: {response.id}", user_id = user_id)
        logger.info(f"Temperature: {request.temperature}", user_id = user_id)
        logger.info(f"Frequency Penalty: {request.frequency_penalty}", user_id = user_id)
        logger.info(f"Presence Penalty: {request.presence_penalty}", user_id = user_id)
        logger.info(f"Max Tokens: {request.max_tokens if request.max_tokens else 'MAX'}", user_id = user_id)
        logger.info(f"Max Completion Tokens: {request.max_completion_tokens if request.max_completion_tokens else 'MAX'}", user_id = user_id)
        
        logger.info("============= Response =============", user_id = user_id)
        if response.system_fingerprint:
            logger.info(f"System Fingerprint: {response.system_fingerprint}", user_id = user_id)
        logger.info(f"Finish Reason: {response.finish_reason}", user_id = user_id)
        logger.info(f"Finish Reason Cause: {response.finish_reason_cause}", user_id = user_id)

        if response.calling_log.total_chunk > 0:
            logger.info("============ Chunk Count ===========", user_id = user_id)
            logger.info(f"Total Chunk: {response.calling_log.total_chunk}", user_id = user_id)
            if response.calling_log.empty_chunk > 0:
                logger.info(f"Empty Chunk: {response.calling_log.empty_chunk}", user_id = user_id)
                logger.info(f"Non-Empty Chunk: {response.calling_log.total_chunk - response.calling_log.empty_chunk}", user_id = user_id)
            logger.info(f"Chunk effective ratio: {1 - response.calling_log.empty_chunk / response.calling_log.total_chunk :.2%}", user_id = user_id)
        
        logger.info("========== Time Statistics =========", user_id = user_id)
        total_time = response.calling_log.stream_processing_end_time.monotonic - response.calling_log.request_start_time.monotonic
        logger.info(f"Total Time: {total_time / 10**9:.2f}s({format_deltatime_ns(total_time, '%H:%M:%S.%f.%u.%n')})", user_id = user_id)
        requests_time = response.calling_log.request_end_time.monotonic - response.calling_log.request_start_time.monotonic
        logger.info(f"API Request Time: {requests_time / 10**9:.2f}s({format_deltatime_ns(requests_time, '%H:%M:%S.%f.%u.%n')})", user_id = user_id)
        stream_processing_time = response.calling_log.stream_processing_end_time.monotonic - response.calling_log.stream_processing_start_time.monotonic
        logger.info(f"Stream Processing Time: {stream_processing_time / 10**9:.2f}s({format_deltatime_ns(stream_processing_time, '%H:%M:%S.%f.%u.%n')})", user_id = user_id)

        created_utc_dt = datetime.fromtimestamp(response.created, tz=timezone.utc)
        created_utc_str = created_utc_dt.strftime('%Y-%m-%d %H:%M:%S UTC')
        logger.info(f"Created Time: {created_utc_str}", user_id = user_id)

        created_local_dt = datetime.fromtimestamp(response.created)
        created_local_str = created_local_dt.strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Created Time: {created_local_str}", user_id = user_id)

        if response.calling_log.total_chunk > 0:
            chunk_nozero_times = [time.monotonic for time in response.calling_log.chunk_times if time.monotonic != 0]
            chunk_average_spawn_time = sum(chunk_nozero_times) // len(chunk_nozero_times)
            max_chunk_spawn_time = max(chunk_nozero_times)
            min_chunk_spawn_time = min(chunk_nozero_times)
            logger.info(f"Chunk Average Spawn Time: {chunk_average_spawn_time / 10**6:.2f}ms({format_deltatime_ns(chunk_average_spawn_time, '%H:%M:%S.%f.%u.%n')})", user_id = user_id)
            logger.info(f"Chunk Max Spawn Time: {max_chunk_spawn_time / 10**6:.2f}ms({format_deltatime_ns(max_chunk_spawn_time, '%H:%M:%S.%f.%u.%n')})", user_id = user_id)
            logger.info(f"Chunk Min Spawn Time: {min_chunk_spawn_time / 10**6:.2f}ms({format_deltatime_ns(min_chunk_spawn_time, '%H:%M:%S.%f.%u.%n')})", user_id = user_id)

        logger.info("=========== Token Count ============", user_id = user_id)
        logger.info(f"Total Tokens: {response.token_usage.total_tokens}", user_id = user_id)
        logger.info(f"Context Input Tokens: {response.token_usage.prompt_tokens}", user_id = user_id)
        logger.info(f"Completion Output Tokens: {response.token_usage.completion_tokens}", user_id = user_id)
        if response.token_usage.prompt_cache_hit_tokens is not None:
            logger.info(f"Cache Hit Count: {response.token_usage.prompt_cache_hit_tokens}", user_id = user_id)
        if response.token_usage.prompt_cache_miss_tokens is not None:
            logger.info(f"Cache Miss Count: {response.token_usage.prompt_cache_miss_tokens}", user_id = user_id)
        if not math.isnan(response.token_usage.prompt_cache_hit_ratio):
            logger.info(f"Cache Hit Ratio: {response.token_usage.prompt_cache_hit_ratio :.2%}", user_id = user_id)
        if response.stream:
            logger.info(f"Average Generation Rate: {response.token_usage.completion_tokens / ((response.calling_log.stream_processing_end_time - response.calling_log.stream_processing_start_time) / 1e9):.2f} /s", user_id = user_id)

        logger.info("============= Content ==============", user_id = user_id)
        logger.info(f"Total Content Length: {response.context.total_length}", user_id = user_id)
        response.calling_log.total_context_length = sum_string_lengths(response.context.full_context, "content")
        logger.info(f"Reasoning Content Length: {len(response.context.last_content.reasoning_content)}", user_id = user_id)
        response.calling_log.reasoning_content_length = len(response.context.last_content.reasoning_content)
        logger.info(f"New Content Length: {len(response.context.last_content.content)}", user_id = user_id)
        response.calling_log.new_content_length = len(response.context.last_content.content)

        logger.info("====================================", user_id = user_id)