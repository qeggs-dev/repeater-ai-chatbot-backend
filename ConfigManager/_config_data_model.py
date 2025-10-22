from pydantic import (
    BaseModel,
    field_validator,
    conint
)
from enum import StrEnum
from typing import Literal, List, Dict, Any

class ItemType(StrEnum):
    INT = "int"
    FLOAT = "float"
    STR = "str"
    STRING = "string"
    BOOL = "bool"
    LIST = "list"
    DICT = "dict"
    JSON = "json"
    YAML = "yaml"
    PATH = "path"
    AUTO = "auto"
    OTHER = "other"

class Config_Item(BaseModel):
    type: ItemType = ItemType.OTHER
    type_name: str | None = None
    system: str | None = None
    environment: str | None = None
    value: Any | None = None

    @field_validator("type_name")
    @classmethod
    def validate_type_name(cls, v, values):
        if v is None:
            return v
        if values["type"] in {ItemType.OTHER, ItemType.AUTO}:
            raise ValueError("type_name cannot be set if type is 'other' or 'auto'")
        return v

class Config_Field(BaseModel):
    name: str
    # version: str
    values: List[Config_Item] | None = None
    annotations: str | None = None