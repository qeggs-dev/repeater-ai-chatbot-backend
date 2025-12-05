from pydantic import BaseModel, ConfigDict, Field

class Bot_Birthday_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    day: int = 28
    month: int = 6
    year: int = 2024

class Bot_Info_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    name: str = "Repeater"
    birthday: Bot_Birthday_Config = Field(default_factory=Bot_Birthday_Config)