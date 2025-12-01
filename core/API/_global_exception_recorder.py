from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from loguru import logger
import traceback
import asyncio
import time
import signal
import os

from ._resource import app
from CriticalException import CriticalException

@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except CriticalException as e:
        # 记录异常日志
        try:
            traceback_info = traceback.format_exc()
            logger.critical("Critical Exception: \n{traceback}", user_id = "[Global Exception Recorder]", traceback = traceback_info)
        except KeyError:
            logger.exception("Exception: {exception}", exception = e)
        # 触发后台任务关闭应用（非阻塞）
        background_tasks = BackgroundTasks()
        background_tasks.add_task(shutdown_server, exception = e)
        return JSONResponse(
            status_code=500,
            content={"error": "A serious error has occurred, the service is about to shut down.", "detail": e.message},
            background=background_tasks,
        )
    except Exception as e:
        # 记录异常日志
        traceback_info = traceback.format_exc()
        logger.exception("An Exception occurred:\n{traceback}", user_id = "[Global Exception Recorder]", traceback = traceback_info)
        return JSONResponse(
            status_code=500,
            content={
                "message": "Internal server error",
                "error": str(e),
                "time": time.time_ns() // 10**6,
            },
        )

async def shutdown_server(exception: CriticalException | None = None) -> None:
    wait_time = None
    if exception is not None:
        if callable(exception.wait):
            try:
                logger.info("Exceptions include waiting callbacks, and programs may exit delayed...", user_id = "[Global Exception Recorder]")
            except KeyError:
                logger.info("[Global Exception Recorder] Exceptions include waiting callbacks, and programs may exit delayed...")
            if asyncio.iscoroutinefunction(exception.wait):
                wait_time: float = await exception.wait(exception)
            elif callable(exception.wait):
                wait_time: float = await asyncio.to_thread(exception.wait, exception)
            elif not isinstance(wait_time, float):
                wait_time: None = None
        elif isinstance(exception.wait, float):
            wait_time: float = exception.wait
    
    if wait_time is not None and (isinstance(wait_time, float) or isinstance(wait_time, int)) and wait_time > 0:
        try:
            logger.info(f"Waiting for {wait_time} seconds before closing the application...", user_id = "[Global Exception Recorder]")
        except KeyError:
            logger.info("[Global Exception Recorder] Waiting for {wait_time} seconds before closing the application...")
        await asyncio.sleep(wait_time)

    logger.critical("正在关闭应用...")
    # 发送 SIGTERM 信号终止进程
    os.kill(os.getpid(), signal.SIGTERM)