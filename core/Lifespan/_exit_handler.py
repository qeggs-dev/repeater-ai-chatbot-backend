from __future__ import annotations
import asyncio
from typing import Coroutine
from ._args import Args
from ._func_obj import FuncObject

class ExitHandler:
    _functions: asyncio.Queue[Coroutine[None, None, None]] = asyncio.Queue()
    _instance: ExitHandler | None = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod 
    async def execute(cls):
        while not cls._functions.empty():
            func = await cls._functions.get()
            await func
    
    @classmethod
    def add_function(cls, func: Coroutine[None, None, None]):
        cls._functions.put_nowait(
            func
        )