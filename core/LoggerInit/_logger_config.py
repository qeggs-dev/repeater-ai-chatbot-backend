from dataclasses import dataclass, field
from ._log_level import LogLevel
from pathlib import Path

@dataclass
class LoggerConfig:
    """
    Logger configuration class
    """
    log_level: LogLevel = LogLevel.INFO
    log_dir: Path = field(default_factory=lambda: Path("./logs"))
    rotation: str = "1 MB"
    log_retention: str = "7 days"
    log_compression: str = "zip"
    log_prefix: str = "repeater_log_"
    log_suffix: str = ".log"