from pydantic import BaseModel, ConfigDict

class Server_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    host: str = "0.0.0.0"
    port: int = 8080
    workers: int = 1
    reload: bool = False