from environs import Env
env = Env()
env.read_env()

import sys
from API import app, configs
from loguru import logger

def main():
    import uvicorn
    host = "0.0.0.0" # 默认监听所有地址
    port = 8000 # 默认监听8000端口

    host = env.str("HOST", host)
    port = env.int("PORT", port)
    workers = env.int("WORKERS", None)
    reload = env.bool("RELOAD", False)

    host = configs.get_config("server.host", host).get_value(str)
    port = configs.get_config("server.port", port).get_value(int)
    workers = configs.get_config("server.workers", workers).get_value(int)
    reload = configs.get_config("server.reload", reload).get_value(bool)

    logger.info(f"Starting server at {host}:{port}")

    if workers:
        logger.info(f"Server will run with {workers} workers")
    
    if reload:
        logger.info("Server will reload on code change")
    
    logger.info(f"Run With {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    logger.info("Server starting...")

    uvicorn.run(
        app = app,
        host = host,
        port = port,
        workers = workers,
        log_config = None,
    )

if __name__ == "__main__":
    main()