from pydantic import BaseModel, Field
from enum import StrEnum
from ._model_type import ModelType

class Model(BaseModel):
    name: str = ""
    id: str = ""
    url: str = ""
    uid: str = ""
    type: ModelType = ModelType.CHAT
    timeout: float | None = None

class ApiInfoConfig(BaseModel):
    name: str = ""
    api_key_env: str = "API_KEY"
    url: str = ""
    models: list[Model] = Field(default_factory=list)
    timeout: float = 60.0
    
class ApiGroup(BaseModel):
    api: list[ApiInfoConfig] = Field(default_factory=list)