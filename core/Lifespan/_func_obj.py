from dataclasses import dataclass
from ._args import Args
from typing import Callable, TypeVar, Generic

T = TypeVar('T', bound=Callable)
T_Args = TypeVar('T_Args', bound=Args)

@dataclass
class FuncObject(Generic[T, T_Args]):
    """A dataclass that represents a function object."""
    args: T_Args
    func: T

    def __call__(self, *args, **kwargs):
        """Calls the function with the given arguments."""
        return self.func(*args, **kwargs)
    
