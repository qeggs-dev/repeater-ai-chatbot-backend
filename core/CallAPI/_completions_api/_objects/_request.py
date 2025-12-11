from dataclasses import dataclass
from typing import Callable
from ._delta import Delta

from ....Context_Manager import ContextObject, CallingFunctionRequest


@dataclass
class Request:
    """
    This class is used to store the request data
    """
    url: str = ""
    key: str = ""
    model: str = ""
    user_name: str | None = None
    temperature: float = 1.0
    top_p: float = 1.0
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    max_tokens: int = 0
    max_completion_tokens: int = 0
    timeout: float = 600.0
    stream: bool = False
    stop: list[str] | None = None
    context: ContextObject | None = None
    logprobs: bool = False
    top_logprobs: int | None = None
    print_chunk: bool = True
    function_calling: CallingFunctionRequest | None = None
    continue_processing_callback_function: Callable[[str, Delta], bool] | None = None