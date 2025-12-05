from pydantic import BaseModel, ConfigDict

class Cache_Data_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    context: bool = False
    prompt: bool = False
    config: bool = False