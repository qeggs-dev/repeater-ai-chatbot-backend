from .._object import Delta, TokensCount
from openai.types.chat import ChatCompletion

async def translation_chunk(
    chunk: ChatCompletion,
) -> Delta:
    """
    翻译单个OpenAI API响应块

    :param chunk: API响应块
    :return: Delta_data对象
    """
    # 初始化对象
    tokens_usage = TokensCount()
    delta_data = Delta()
    # 转录ID
    if hasattr(chunk, "id"):
        delta_data.id = chunk.id
    # 转录创建时间
    if hasattr(chunk, "created"):
        delta_data.created = chunk.created
    # 转录模型名称
    if hasattr(chunk, "model"):
        delta_data.model = chunk.model
    
    # 转录内容
    if hasattr(chunk, "choices") and len(chunk.choices) > 0:
        choice = chunk.choices[0]
        if hasattr(choice, "delta"):
            # 转录推理内容
            if hasattr(choice.delta, "reasoning_content"):
                reasoning_data = choice.delta.reasoning_content
                if reasoning_data is not None:
                    delta_data.reasoning_content = reasoning_data

            # 转录响应内容
            if hasattr(choice.delta, "content"):
                content = choice.delta.content
                if content:
                    delta_data.content = content
            
            # 转录工具调用
            if hasattr(choice.delta, "tool_calls"):
                content = choice.delta.tool_calls
                if content:
                    tool = content[0]
                    if hasattr(tool, "id"):
                        delta_data.function_id = tool.id
                    if hasattr(tool, "type"):
                        delta_data.function_type = tool.type
                    if hasattr(tool, "function"):
                        if hasattr(tool.function, "name"):
                            delta_data.function_name = tool.function.name
                        if hasattr(tool.function, "arguments"):
                            delta_data.function_arguments = tool.function.arguments
        
        if hasattr(choice, "finish_reason"):
            delta_data.finish_reason = choice.finish_reason
            
    if hasattr(chunk, "system_fingerprint"):
        delta_data.system_fingerprint = chunk.system_fingerprint

    # 转录usage数据
    if hasattr(chunk, 'usage') and chunk.usage is not None:
        # 只在最后一个chunk中获取usage数据
        if hasattr(chunk.usage, 'prompt_tokens') and chunk.usage.prompt_tokens is not None:
            tokens_usage.prompt_tokens = chunk.usage.prompt_tokens
        if hasattr(chunk.usage, 'completion_tokens') and chunk.usage.completion_tokens is not None:
            tokens_usage.completion_tokens = chunk.usage.completion_tokens
        if hasattr(chunk.usage, 'total_tokens') and chunk.usage.total_tokens is not None:
            tokens_usage.total_tokens = chunk.usage.total_tokens
        if hasattr(chunk.usage, 'prompt_cache_hit_tokens') and chunk.usage.prompt_cache_hit_tokens is not None:
            tokens_usage.prompt_cache_hit_tokens = chunk.usage.prompt_cache_hit_tokens
        if hasattr(chunk.usage, 'prompt_cache_miss_tokens') and chunk.usage.prompt_cache_miss_tokens is not None:
            tokens_usage.prompt_cache_miss_tokens = chunk.usage.prompt_cache_miss_tokens
    
    delta_data.token_usage = tokens_usage

    return delta_data