from ConfigManager import ConfigLoader as GlobalConfigLoader
from ._logger_config import LoggerConfig
from pathlib import Path
from ._log_level import LogLevel


class ConfigLoader:
    configs = GlobalConfigLoader()
    last_loaded_config: LoggerConfig | None = None

    @classmethod
    def load_config(cls) -> LoggerConfig:
        cls.last_loaded_config = LoggerConfig(
            log_level = LogLevel[cls.configs.get_config("logger.log_level", "INFO").get_value(str)],
            log_dir = cls.configs.get_config("logger.log_file_dir", "./logs").get_value(Path),
            rotation = cls.configs.get_config("logger.rotation", "1 MB").get_value(str),
            log_retention = cls.configs.get_config("logger.log_retention", "10 days").get_value(str),
            log_compression = cls.configs.get_config("logger.compression", "zip").get_value(str),
            log_prefix = cls.configs.get_config("logger.log_file_prefix", "repeater_log_").get_value(str),
            log_suffix = cls.configs.get_config("logger.log_file_suffix", "").get_value(str),
        )
        return cls.last_loaded_config