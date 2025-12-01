from pydantic import BaseModel, ConfigDict


class Backlist_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    file_path: str = "./config/backlist.json"
    match_timeout: float = 10