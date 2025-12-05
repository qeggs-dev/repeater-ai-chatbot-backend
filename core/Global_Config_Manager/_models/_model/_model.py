from pydantic import BaseModel, ConfigDict, Field

class Model_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    default_temperature: float = Field(0.7, ge = 0.0, le = 2.0)
    default_top_p: float = Field(1.0, ge=0.0, le=1.0)
    default_max_tokens: int = 4096
    default_max_completion_tokens: int = 4096
    default_frequency_penalty: float = Field(0.0, ge = -2.0, le = 2.0)
    default_presence_penalty: float = Field(0.0, ge = -2.0, le = 2.0)
    default_stop: list[str] = Field(default_factory = list)
    stream: bool = True