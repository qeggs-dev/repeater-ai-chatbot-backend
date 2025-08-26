from dataclasses import dataclass, field
from ._exceptions import *
from typing import Literal

from environs import Env, EnvError

env = Env()

@dataclass
class ApiGroup:
    url: str = ""
    api_key_envname: str = ""
    group_name: str = ""
    model_name: str = ""
    model_id: str = ""
    request_type: Literal["GET", "POST", "PUT", "DELETE", "PATCH"] | None = "GET"
    model_uid: str = ""
    task_type: str = ""
    metadata: dict = field(default_factory=dict)

    @property
    def api_key(self) -> str:
        try:
            return env.str(self.api_key_envname, '')
        except EnvError:
            raise APIKeyNotSetError(f"API key for {self.group_name} not set. Please set the environment variable {self.api_key_envname}.")