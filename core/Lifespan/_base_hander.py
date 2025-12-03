from __future__ import annotations
import asyncio
from typing import Callable, Awaitable

class Handler:
    _functions: asyncio.Queue[Callable[[], Awaitable[None]]] = asyncio.Queue()
    _instance: Handler | None = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    async def execute(cls):
        while not cls._functions.empty():
            func: Callable[[], Awaitable[None]] = await cls._functions.get()
            await func()
    
    @classmethod
    def add_function(cls, func: Callable[[], Awaitable[None]]):
        cls._functions.put_nowait(func)