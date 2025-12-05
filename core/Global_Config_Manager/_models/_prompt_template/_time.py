from pydantic import BaseModel, ConfigDict

class Time_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    time_offset: float = 0.0