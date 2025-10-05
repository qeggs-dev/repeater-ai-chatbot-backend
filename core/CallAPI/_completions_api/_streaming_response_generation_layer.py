from typing import AsyncGenerator, Self
from ._object import Request, Delta, Response
from ..CallLog import CallLog
from ..Context import ContentUnit, ContextRole, FunctionResponseUnit
from ..CallLog import TimeStamp
from loguru import logger

class StreamingResponseGenerationLayer:
    """
    Delta 生成流包装器

    用于在流式响应中创建统计夹层以恢复非流式调用时的统计功能

    ---

    :param user_id: 用户ID
    :param request: 请求对象
    :param response_iterator: 原始响应迭代器
    """
    def __init__(self, user_id: str, request: Request, response_iterator: AsyncGenerator[Delta, None]) -> None:
        self.request: Request = request
        self._response_iterator: AsyncGenerator[Delta, None] = response_iterator
        self._finished: bool = False
        # ==== Initialize the response object ==== #
        
        # 创建响应对象
        self.response = Response()
        # 创建调用日志
        self.response.calling_log = CallLog()

        # 设置用户ID
        self.user_id = user_id
        

        # 写入调用日志基础信息
        self.response.calling_log.url = self.request.url
        self.response.calling_log.user_id = self.user_id
        self.response.calling_log.user_name = self.request.user_name
        self.response.calling_log.model = self.request.model
        self.response.calling_log.stream = self.request.stream

        # 如果context为空，则抛出异常
        if not self.request.context:
            raise ValueError("context is required")
        
        # 请求流式连接
        logger.info(f"Start Connecting to the API", user_id = self.user_id)
        self.request_start_time = TimeStamp()
        self.request_end_time = TimeStamp()

        # 创建响应缓冲区单元
        self.model_response_content_unit:ContentUnit = ContentUnit()
        # 设置角色
        self.model_response_content_unit.role = ContextRole.ASSISTANT
        # chunk计数器
        self.chunk_count:int = 0
        # 空chunk计数器
        self.empty_chunk_count:int = 0

        # 开始处理流式响应
        logger.info(f"Start Streaming", user_id = self.user_id)
        print("\n", end="", flush=True)
        # 记录流开始时间
        # 记录上次chunk时间
        self.last_chunk_time:TimeStamp = TimeStamp(0,0)
        self.created:TimeStamp = TimeStamp()
        # chunk耗时列表
        self.chunk_times:list[TimeStamp] = []
    
    def finally_stream(self):
        print('\n\n', end="", flush=True)

        # 添加日志统计数据
        self.response.calling_log.id = self.response.id
        self.response.calling_log.total_chunk = self.chunk_count
        self.response.calling_log.empty_chunk = self.empty_chunk_count
        self.response.calling_log.request_start_time = self.request_start_time
        self.response.calling_log.request_end_time = self.request_end_time
        self.response.calling_log.chunk_times = self.chunk_times
        self.response.calling_log.total_tokens = self.response.token_usage.total_tokens
        self.response.calling_log.prompt_tokens = self.response.token_usage.prompt_tokens
        self.response.calling_log.completion_tokens = self.response.token_usage.completion_tokens
        self.response.calling_log.cache_hit_count = self.response.token_usage.prompt_cache_hit_tokens
        self.response.calling_log.cache_miss_count = self.response.token_usage.prompt_cache_miss_tokens

        # 添加上下文
        self.response.context = self.request.context
        self.response.context.context_list.append(self.model_response_content_unit)

    def __aiter__(self) -> Self:
        """
        Returns the streaming response generation layer as an iterator.
        """
        stream_processing_start_time:int = TimeStamp()
        self.response.calling_log.stream_processing_start_time = stream_processing_start_time
        return self

    async def __anext__(self) -> Delta:
        """
        Returns the next chunk of data from the streaming response generation layer.
        """
        try:
            delta_data = await anext(self._response_iterator)
            self._parse_delta(delta_data)
            return delta_data
        except StopAsyncIteration as e:
            if not self._finished:
                self._finished = True
            stream_processing_end_time: int = TimeStamp()
            self.response.calling_log.stream_processing_end_time = stream_processing_end_time
            self.finally_stream()
            raise e
    
    def _parse_delta(self, delta_data: Delta):
        # 记录会话开启时间
        if not self.response.created:
            self.response.created = delta_data.created
        
        # 记录chunk时间
        if self.last_chunk_time == TimeStamp(0,0):
            self.last_chunk_time = TimeStamp()
        else:
            this_chunk_time = TimeStamp()
            time_difference = this_chunk_time - self.last_chunk_time
            self.chunk_times.append(time_difference)
            self.last_chunk_time = this_chunk_time
        
        # 记录会话ID
        if not self.response.id:
            self.response.id = delta_data.id
        
        # 记录模型名称
        if not self.response.model:
            self.response.model = delta_data.model
        
        # 记录token使用情况
        if delta_data.token_usage:
            self.response.token_usage = delta_data.token_usage

        # 记录模型推理响应内容
        if delta_data.reasoning_content:
            if self.request.print_chunk:
                if not self.model_response_content_unit.reasoning_content:
                    print('\n\n', end="", flush=True)
                print(f"\033[7m{delta_data.reasoning_content}\033[0m", end="", flush=True)
                logger.bind(donot_send_console=True).debug("Received Reasoning_Content chunk: {reasoning_content}", user_id = self.user_id, reasoning_content = repr(delta_data.reasoning_content))
            self.model_response_content_unit.reasoning_content += delta_data.reasoning_content
        
        # 记录模型响应内容
        if delta_data.content:
            if self.request.print_chunk:
                if not self.model_response_content_unit.content:
                    print('\n\n', end="", flush=True)
                print(delta_data.content, end="", flush=True)
                logger.bind(donot_send_console=True).debug("Received Content chunk: {content}", user_id = self.user_id, content = repr(delta_data.content))
            self.model_response_content_unit.content += delta_data.content
        
        # 记录模型工具调用内容
        if delta_data.function_id:
            self.model_response_content_unit.funcResponse.callingFunctionResponse.append(
                FunctionResponseUnit(
                    id = delta_data.function_id,
                    type = delta_data.function_type,
                    name = delta_data.function_name,
                    arguments_str = delta_data.function_arguments,
                )
            )
        
        if delta_data.system_fingerprint:
            self.response.system_fingerprint = delta_data.system_fingerprint

        # 判断是否为空并增加空chunk计数器
        if delta_data.is_empty:
            self.empty_chunk_count += 1
        self.chunk_count += 1

        # 处理回调函数
        if self.request.continue_processing_callback_function is not None:
            if self.request.continue_processing_callback_function(self.user_id, delta_data):
                self._response_iterator.aclose()
                raise StopIteration
    @property
    def is_finished(self) -> bool:
        """
        Returns True if the streaming response generation layer has finished yielding data.
        """
        return self._finished