from pydantic import BaseModel, ConfigDict

class Logger_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    file_path: str = "./logs/repeater-log-{time:%Y-%m-%d-%H-%M-%S}.log"
    level: str = "INFO"
    rotation: str = "10 MB"
    retention: str = "7 days"
    compression: str = "zip"