from dataclasses import dataclass
from environs import Env
from ._model_type import ModelType

_env = Env()


@dataclass
class ApiObject:
    name: str = ""
    url: str = ""
    id: str = ""
    api_key_env: str = "API_KEY"
    parent: str = ""
    uid: str = ""
    type: ModelType = ModelType.CHAT
    timeout: float = 60.0

    @property
    def api_key(self) -> str:
        return _env.str(self.api_key_env, "None")