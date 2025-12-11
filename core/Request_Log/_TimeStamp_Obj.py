from __future__ import annotations
from pydantic import BaseModel, ConfigDict, Field
import time

class TimeStamp(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
    )

    time_stamp: int = Field(default_factory=lambda: time.time_ns())
    monotonic: int = Field(default_factory=lambda: time.monotonic_ns())

    def record(self, update_time: bool = True, update_monotonic: bool = True) -> None:
        """
        Record the current time
        """
        if update_time:
            self.time_stamp = time.time_ns()
        if update_monotonic:
            self.monotonic = time.monotonic_ns()
    
    def __add__(self, other: TimeStamp | int) -> TimeStamp:
        if isinstance(other, TimeStamp):
            return TimeStamp(
                time_stamp = self.time_stamp + other.time_stamp,
                monotonic = self.monotonic + other.monotonic
            )
        elif isinstance(other, int):
            other = TimeStamp(
                time_stamp = self.time_stamp + other,
                monotonic = self.monotonic + other
            )
        else:
            return NotImplemented
    
    def __radd__(self, other: TimeStamp | int) -> TimeStamp:
        if isinstance(other, TimeStamp):
            return TimeStamp(
                other.time_stamp + self.time_stamp,
                other.monotonic + self.monotonic
            )
        elif isinstance(other, int):
            other = TimeStamp(
                time_stamp = other + self.time_stamp,
                monotonic = other + self.monotonic
            )
        else:
            return NotImplemented
    
    def __iadd__(self, other: TimeStamp | int) -> TimeStamp:
        if isinstance(other, TimeStamp):
            self.time_stamp += other.time_stamp
            self.monotonic += other.monotonic
            return self
        elif isinstance(other, int):
            self.time_stamp += other
            self.monotonic += other
            return self
        else:
            return NotImplemented
    
    def __sub__(self, other: TimeStamp | int) -> TimeStamp:
        if isinstance(other, TimeStamp):
            return TimeStamp(
                self.time_stamp - other.time_stamp,
                self.monotonic - other.monotonic
            )
        elif isinstance(other, int):
            return TimeStamp(
                self.time_stamp - other,
                self.monotonic - other
            )
        else:
            return NotImplemented
    
    def __rsub__(self, other: TimeStamp | int) -> TimeStamp:
        if isinstance(other, TimeStamp):
            return TimeStamp(
                other.time_stamp - self.time_stamp,
                other.monotonic - self.monotonic
            )
        elif isinstance(other, int):
            return TimeStamp(
                other - self.time_stamp,
                other - self.monotonic
            )
        else:
            return NotImplemented
    
    def __isub__(self, other: TimeStamp | int) -> TimeStamp:
        if isinstance(other, TimeStamp):
            self.time_stamp -= other.time_stamp
            self.monotonic -= other.monotonic
            return self
        elif isinstance(other, int):
            self.time_stamp -= other
            self.monotonic -= other
            return self
        else:
            return NotImplemented
    
    def __mul__(self, other: TimeStamp | int) -> TimeStamp:
        if isinstance(other, TimeStamp):
            return TimeStamp(
                self.time_stamp * other.time_stamp,
                self.monotonic * other.monotonic,
            )
        elif isinstance(other, int):
            return TimeStamp(
                self.time_stamp * other,
                self.monotonic * other,
            )
        else:
            return NotImplemented
    
    def __rmul__(self, other: TimeStamp | int) -> TimeStamp:
        if isinstance(other, TimeStamp):
            return TimeStamp(
                other.time_stamp * self.time_stamp,
                other.monotonic * self.monotonic,
            )
        elif isinstance(other, int):
            return TimeStamp(
                other * self.time_stamp,
                other * self.monotonic,
            )
        else:
            return NotImplemented
    
    def __imul__(self, other: TimeStamp | int) -> TimeStamp:
        if isinstance(other, TimeStamp):
            self.time_stamp *= other.time_stamp
            self.monotonic *= other.monotonic
            return self
        elif isinstance(other, int):
            self.time_stamp *= other
            self.monotonic *= other
            return self
        else:
            return NotImplemented
    
    def __floordiv__(self, other: TimeStamp | int) -> TimeStamp:
        if isinstance(other, TimeStamp):
            return TimeStamp(
                self.time_stamp // other.time_stamp,
                self.monotonic // other.monotonic,
            )
        elif isinstance(other, int):
            return TimeStamp(
                self.time_stamp // other,
                self.monotonic // other,
            )
        else:
            return NotImplemented
    
    def __truediv__(self, other: TimeStamp | int) -> TimeStamp:
        return NotImplemented
    
    def __rtruediv__(self, other: TimeStamp | int) -> TimeStamp:
        return NotImplemented
    
    def __rfloordiv__(self, other: TimeStamp | int) -> TimeStamp:
        if isinstance(other, TimeStamp):
            return TimeStamp(
                other.time_stamp // self.time_stamp,
                other.monotonic // self.monotonic,
            )
        elif isinstance(other, int):
            return TimeStamp(
                other // self.time_stamp,
                other // self.monotonic,
            )
        else:
            return NotImplemented
    
    def __itruediv__(self, other: TimeStamp | int) -> TimeStamp:
        return NotImplemented
    
    def __ifloordiv__(self, other: TimeStamp | int) -> TimeStamp:
        if isinstance(other, TimeStamp):
            self.time_stamp //= other.time_stamp
            self.monotonic //= other.monotonic
            return self
        elif isinstance(other, int):
            self.time_stamp //= other
            self.monotonic //= other
            return self
        else:
            return NotImplemented
    
    def __mod__(self, other: TimeStamp | int) -> TimeStamp:
        return TimeStamp(self.time_stamp % other.time_stamp, self.monotonic % other.monotonic)
    
    def __rmod__(self, other: TimeStamp | int) -> TimeStamp:
        return TimeStamp(other.time_stamp % self.time_stamp, other.monotonic % self.monotonic)
    
    def __imod__(self, other: TimeStamp | int) -> TimeStamp:
        self.time_stamp %= other.time_stamp
        self.monotonic %= other.monotonic
        return self
    
    def __pow__(self, other: TimeStamp | int) -> TimeStamp:
        return TimeStamp(self.time_stamp ** other.time_stamp, self.monotonic ** other.monotonic)
    
    def __rpow__(self, other: TimeStamp | int) -> TimeStamp:
        return TimeStamp(other.time_stamp ** self.time_stamp, other.monotonic ** self.monotonic)

    def __ipow__(self, other: TimeStamp | int) -> TimeStamp:
        self.time_stamp **= other.time_stamp
        self.monotonic **= other.monotonic
        return self
    
    def __neg__(self) -> TimeStamp:
        return TimeStamp(-self.time_stamp, -self.monotonic)
    
    def __pos__(self) -> TimeStamp:
        return TimeStamp(+self.time_stamp, +self.monotonic)
    
    def __abs__(self) -> TimeStamp:
        return TimeStamp(abs(self.time_stamp), abs(self.monotonic))
    
    def __eq__(self, other: TimeStamp) -> bool:
        return self.time_stamp == other.time_stamp and self.monotonic == other.monotonic
    
    def __ne__(self, other: TimeStamp) -> bool:
        return self.time_stamp != other.time_stamp or self.monotonic != other.monotonic
    
    def __hash__(self) -> int:
        return hash((self.time_stamp, self.monotonic))
    
    def __repr__(self) -> str:
        return f"TimeStamp({self.time_stamp}, {self.monotonic})"