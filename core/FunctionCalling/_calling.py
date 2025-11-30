import asyncio
from typing import Any, Callable, Awaitable, Protocol, runtime_checkable
from ..Context import CallingFunctionResponse, ContextSyntaxError, ContentUnit, ContextRole
from ._exceptions import *

@runtime_checkable
class SupportsStr(Protocol):
    def __str__(self) -> str:
        ...

class FunctionCalling:
    """
    FunctionCalling对象
    
    用于提供函数调用功能，并尝试自动转换类型
    """
    def __init__(self):
        self._function_calling_map: dict[str, Callable[..., Awaitable[SupportsStr]]] = {}
        self._function_calling_args_types: dict[str, dict[str, type | Callable[[str], object]]] = {}
        self._global_resource_lock = asyncio.Lock()
    
    async def register(self, function: Callable[..., Awaitable[SupportsStr]], funcargs_types: dict[str, type | Callable[[str], object]] | None = None, name: str | None = None):
        """
        注册一个函数调用
        
        :param function: 函数调用
        :param funcargs_types: 函数参数类型
        :param name: 函数调用名称
        """
        async with self._global_resource_lock:
            if not asyncio.iscoroutinefunction(function):
                raise TypeError("function must be a coroutine function")
            self._function_calling_map[name or function.__name__] = function
            if funcargs_types:
                self._function_calling_args_types[name or function.__name__] = funcargs_types
    
    async def call(self, calling_function: CallingFunctionResponse) -> ContentUnit:
        for function_response in calling_function.callingFunctionResponse:
            id = function_response.id
            name = function_response.name
            try:
                arguments:dict = function_response.load_arguments()
            except ContextSyntaxError:
                raise FunctionCallingArgumentsSyntaxError(f"FunctionCalling {id} {name} arguments syntax error")
            
            if not isinstance(arguments, dict):
                raise ContextSyntaxError("FunctionCalling arguments must be a dict")
            
            async with self._global_resource_lock:
                if name not in self._function_calling_map:
                    raise FunctionNotFound(f"FunctionCalling {id} {name} not found")

                function = self._function_calling_map[name]
                if name in self._function_calling_args_types:
                    args = self._function_calling_args_types[name]
                    typed_arguments = {}
                    for argname, argvalue in arguments.items():
                        if argname not in args:
                            raise FunctionArgumentsTypeError(f"FunctionCalling {id} {name} arguments type error")
                        argtype = args[argname]
                        try:
                            typed_arguments[argname] = argtype(argvalue)
                        except Exception as e:
                            raise FunctionArgumentsValueAutoTypeError(f"FunctionCalling {id} {name} arguments value auto type error: {e}")
                    arguments = typed_arguments
            try:
                result = await function(**arguments)
            except Exception as e:
                raise FunctionCallingException(f"FunctionCalling {id} {name} error: {e}")
            else:
                return ContentUnit(content=str(result), role=ContextRole.FUNCTION, tool_call_id=id)
    
    async def unregister(self, name: str):
        """
        注销一个函数调用
        
        :param name: 函数调用名称
        """
        async with self._global_resource_lock:
            if name in self._function_calling_args_types:
                del self._function_calling_args_types[name]
            if name in self._function_calling_map:
                del self._function_calling_map[name]