from pydantic import BaseModel, ConfigDict

class Server_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    host: str | None = None
    port: int | None = None
    workers: int | None = None
    reload: bool | None = None
    error_message: str = "Internal Server Error"
    critical_error_message: str = "Critical Server Error, Server will shutdown."