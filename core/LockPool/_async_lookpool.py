from __future__ import annotations
import asyncio
from typing import TypeVar

T_KEY = TypeVar('T_KEY')

class LockPool:
    def __init__(self):
        self._lock = asyncio.Lock()
        self.locks: dict[T_KEY, asyncio.Lock] = {}
        self._reference_count : dict[T_KEY, int] = {}
    
    
    async def get_lock(self, key: T_KEY) -> asyncio.Lock:
        async with self._lock:
            if key in self.locks:
                return self.locks[key]
            class Packaged_Lock(asyncio.Lock):
                def _increase_reference_counting(inner_self):
                    if key not in self._reference_count:
                        if key not in self.locks:
                            self.locks[key] = inner_self
                        self._reference_count[key] = 1
                    else:
                        self._reference_count[key] += 1
                
                def _reduce_reference_counting(inner_self):
                    if self._reference_count[key] > 0:
                        self._reference_count[key] -= 1
                    else:
                        if key in self.locks:
                            del self.locks[key]
                        del self._reference_count[key]
                
                async def acquire(inner_self):
                    inner_self._increase_reference_counting()
                    try:
                        await super().acquire()
                    except Exception as e:
                        inner_self._reduce_reference_counting()
                        raise
                def release(inner_self):
                    super().release()
                    inner_self._reduce_reference_counting()
            
            lock = Packaged_Lock()
            self.locks[key] = lock
            return lock
    async def lock_count(self, key: T_KEY):
        async with self._lock:
            return self._reference_count.get(key, 0)
    def __contains__(self, key: T_KEY) -> bool:
        return key in self.locks
    def __len__(self) -> int:
        return len(self.locks)