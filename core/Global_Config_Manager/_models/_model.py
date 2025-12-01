from pydantic import BaseModel, ConfigDict, Field

class Model_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    default_model_uid: str = "chat"
    default_temperature: float = 1.0
    default_top_p: float = 1.0
    default_max_tokens: int = 4096
    default_max_completion_tokens: int = 4096
    default_frequency_penalty: float = 0.0
    default_presence_penalty: float = 0.0
    default_stop: list[str] = Field(default_factory=list)
    stream: bool = True