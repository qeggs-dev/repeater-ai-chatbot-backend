from dataclasses import dataclass, asdict

@dataclass
class Request_User_Info:
    username: str | None = None
    nickname: str | None = None
    age: int | None = None
    gender: str | None = None

    @property
    def as_dict(self) -> dict:
        return asdict(self)