from typing import overload, Literal, AsyncIterator, Callable, Awaitable
from abc import ABC, abstractmethod
from .._object import Request, Response, Delta

class BaseCallAPI(ABC):
    """
    Abstract class for calling API
    """
    @abstractmethod
    async def call(self, user_id: str, request: Request) -> Response | AsyncIterator[Delta]:
        pass

    @property
    @abstractmethod
    def streamable(self) -> bool:
        pass

class CallNstreamAPIBase(BaseCallAPI, ABC):
    """
    Base class for calling non-streaming API
    """
    @property
    def streamable(self) -> Literal[False]:
        return False

    @abstractmethod
    async def call(self, user_id: str, request: Request) -> Response:
        pass

class CallStreamAPIBase(BaseCallAPI, ABC):
    """
    Base class for calling streaming API
    """
    @property
    def streamable(self) -> Literal[True]:
        return True

    @abstractmethod
    async def call(self, user_id: str, request: Request) -> AsyncIterator[Delta]:
        pass