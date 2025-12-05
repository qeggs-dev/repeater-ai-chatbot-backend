from pydantic import BaseModel, ConfigDict

class Web_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    index_web_file: str = ""