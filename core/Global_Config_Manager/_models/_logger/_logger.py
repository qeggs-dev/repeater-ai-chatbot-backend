from pydantic import BaseModel, ConfigDict
from ._log_level import LogLevel

class Logger_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    file_path: str = "./logs/repeater-log-{time:YYYY-MM-DD_HH-mm-ss.SSS}.log"
    level: LogLevel = LogLevel.DEBUG
    rotation: str = "10 MB"
    retention: str = "7 days"
    compression: str = "zip"