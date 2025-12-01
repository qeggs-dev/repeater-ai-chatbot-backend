from pydantic import BaseModel, ConfigDict

class Core_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    version: str = ""