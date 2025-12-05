from pydantic import BaseModel, ConfigDict, Field

class Preprocess_Map_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    before: dict[str, str] = Field(default_factory=dict)
    after: dict[str, str] = Field(default_factory=dict)