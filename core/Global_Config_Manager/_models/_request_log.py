from pydantic import BaseModel, ConfigDict

class Request_Log_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    dir: str = "./workspace/request_log"
    auto_save: bool = True
    debonce_save_wait_time: float = 1200.0
    max_cache_size: int = 1000