from environs import Env
env = Env()
env.read_env()

import uvicorn
import sys
from core import (
    Global_Config_Manager as Global_Config,
    API as Core_API,
    __version__ as core_version,
    __api_version__ as core_api_version,
)
from loguru import logger

def main():
    host = "0.0.0.0" # 默认监听所有地址
    port = 8000 # 默认监听8000端口

    host = env.str("HOST", host)
    port = env.int("PORT", port)
    workers = env.int("WORKERS", None)
    reload = env.bool("RELOAD", False)

    host = Global_Config.ConfigManager.get_configs().server.host or host
    port = Global_Config.ConfigManager.get_configs().server.port or port
    workers = Global_Config.ConfigManager.get_configs().server.workers or workers
    reload = Global_Config.ConfigManager.get_configs().server.reload or reload

    logger.info(f"Starting server at {host}:{port}")

    if workers:
        logger.info(f"Server will run with {workers} workers")
    
    if reload:
        logger.info("Server will reload on code change")
    
    logger.info(f"Run With Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    logger.info(f"Core Version: {core_version}")
    logger.info(f"Core API Version: {core_api_version}")
    
    logger.info("Server starting...")

    uvicorn.run(
        app = Core_API.app,
        host = host,
        port = port,
        workers = workers,
        log_config = None,
    )

if __name__ == "__main__":
    main()