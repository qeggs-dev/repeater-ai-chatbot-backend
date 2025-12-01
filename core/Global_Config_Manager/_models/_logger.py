from pydantic import BaseModel, ConfigDict
from enum import StrEnum

class LogLevel(StrEnum):
    """Logger log levels."""
    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class Logger_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    file_path: str = "./logs/repeater-log-{time:YYYY-MM-DD_HH-mm-ss.SSS}.log"
    level: LogLevel = LogLevel.INFO
    rotation: str = "10 MB"
    retention: str = "7 days"
    compression: str = "zip"