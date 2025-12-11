from pydantic import BaseModel, Field
from typing import Any
from ._TimeStamp_Obj import TimeStamp

class RequestLogObject(BaseModel):
    """
    Class to represent a request log object.
    """
    id: str = ""
    url: str = ""
    model: str = ""
    user_id: str = ""
    user_name: str = ""
    stream: bool = True

    total_chunk: int = 0
    empty_chunk: int = 0

    task_start_time: TimeStamp = Field(default_factory=lambda: TimeStamp(0,0))
    task_end_time: TimeStamp = Field(default=lambda: TimeStamp(0,0))
    request_start_time: TimeStamp = Field(default_factory=lambda: TimeStamp(0,0))
    request_end_time: TimeStamp = Field(default_factory=lambda: TimeStamp(0,0))
    stream_processing_start_time: TimeStamp = Field(default_factory=lambda: TimeStamp(0,0))
    stream_processing_end_time: TimeStamp = Field(default_factory=lambda: TimeStamp(0,0))
    call_prepare_start_time: TimeStamp = Field(default_factory=lambda: TimeStamp(0,0))
    call_prepare_end_time: TimeStamp = Field(default_factory=lambda: TimeStamp(0,0))
    chunk_times: list[TimeStamp] = Field(default_factory=list)
    created_time: TimeStamp = 0

    total_tokens: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    cache_hit_count: int = 0
    cache_miss_count: int = 0

    total_context_length: TimeStamp = 0
    reasoning_content_length: TimeStamp = 0
    new_content_length: TimeStamp = 0
    

class CallAPILogObject(BaseModel):
    """
    Class to represent a call API log object.
    """
    source: str = ""
    start_time: TimeStamp = Field(default_factory=lambda: TimeStamp(0,0))
    end_time: TimeStamp = Field(default_factory=lambda: TimeStamp(0,0))
    user_id: str = ""