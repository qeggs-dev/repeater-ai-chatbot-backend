import sys
import logging
from pathlib import Path
from loguru import logger
from ConfigManager import ConfigLoader
from ._intercept_handler import InterceptHandler

configs = ConfigLoader()

def logger_init():
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(logging.INFO)

    # 移除其他日志处理器
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # 移除默认处理器
    logger.remove()
    log_level = configs.get_config("logger.log_level", "INFO").get_value(str)
    # 添加自定义处理器
    logger.add(
        sys.stderr,
        format = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{extra[user_id]}</cyan> - <level>{message}</level>",
        filter = lambda record: "donot_send_console" not in record["extra"],
        level = log_level
    )

    log_dir = configs.get_config("logger.log_file_dir", "./logs").get_value(Path)
    rotation = configs.get_config("logger.rotation", "1 MB").get_value(str)
    log_retention = configs.get_config("logger.log_retention", "10 days").get_value(str)
    log_compression = configs.get_config("logger.compression", "zip").get_value(str)
    if not log_dir.exists():
        log_dir.mkdir(parents=True, exist_ok=True)
    log_prefix = configs.get_config("logger.log_file_prefix", "repeater_log_").get_value(str)
    log_file = log_dir / (log_prefix + "{time:YYYY-MM-DD_HH-mm-ss.SSS}.log")
    logger.add(
        log_file,
        format = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {extra[user_id]} - {message}",
        level = log_level,
        enqueue = True,
        delay = True,
        rotation = rotation,
        retention = log_retention,
        compression = log_compression,
    )
    logger.configure(
        extra={
            "user_id": "[System]"
        }
    )