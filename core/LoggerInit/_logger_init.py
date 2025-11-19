import sys
import logging
from pathlib import Path
from loguru import logger
from ConfigManager import ConfigLoader
from ._intercept_handler import InterceptHandler
from ._logger_config import LoggerConfig
def logger_init(config: LoggerConfig):
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(logging.INFO)

    # 移除其他日志处理器
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # 移除默认处理器
    logger.remove()
    # 添加自定义处理器
    logger.add(
        sys.stderr,
        format = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{extra[user_id]}</cyan> - <level>{message}</level>",
        filter = lambda record: "donot_send_console" not in record["extra"],
        level = config.log_level.value
    )

    if not config.log_dir.exists():
        config.log_dir.mkdir(parents=True, exist_ok=True)
    
    log_prefix = config.log_prefix
    log_suffix = config.log_suffix
    log_file = config.log_dir / (log_prefix + "{time:YYYY-MM-DD_HH-mm-ss.SSS}" + log_suffix)
    logger.add(
        log_file,
        format = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {extra[user_id]} - {message}",
        level = config.log_level.value,
        enqueue = True,
        delay = True,
        rotation = config.rotation,
        retention = config.log_retention,
        compression = config.log_compression,
    )

    logger.configure(
        extra={
            "user_id": "[System]"
        }
    )