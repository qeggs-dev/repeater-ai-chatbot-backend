import os
import copy
import orjson
import asyncio
import aiofiles
import datetime
import numpy as np
from pathlib import Path
from loguru import logger
from ConfigManager import ConfigLoader
from typing import List, AsyncIterator, Generator, Iterable
from ._RequestLogObject import RequestLogObject, CallAPILogObject

configs = ConfigLoader()

class RequestLogManager:
    def __init__(
            self,
            base_dir: os.PathLike | str,
            debonce_save_wait_time: float | None = None,
            max_cache_size: int | None = None,
            auto_save: bool = True
        ):
        # 日志缓存列表
        self._log_list: List[RequestLogObject | CallAPILogObject] = []

        # 防抖保存等待时间
        if debonce_save_wait_time is None:
            debonce_save_wait_time = configs.get_config("request_log.debonce.save_wait_time", 1200.0).get_value(float)
        self._debonce_save_wait_time:float = debonce_save_wait_time

        # 最大缓存大小
        if max_cache_size is None:
            max_cache_size = configs.get_config("request_log.max_cache_size", 1000).get_value(int)
        self._max_cache_size = max_cache_size

        # 日志文件路径
        self._base_dir = Path(base_dir)
        if self._base_dir.exists():
            if not self._base_dir.is_dir():
                raise ValueError(f"Invalid path \"{self._base_dir}\"")
        else:
            # 确保日志目录存在
            self._base_dir.mkdir(parents=True, exist_ok=True)

        # 日志锁
        self._async_lock = asyncio.Lock()

        # 防抖任务
        self._debonce_task: asyncio.Task | None = None

        # 自动保存
        self._auto_save: bool = auto_save
    
    @property
    def log_file_path(self) -> Path:
        """
        日志文件路径
        """
        time = datetime.datetime.now()
        return self._base_dir / f"{time.strftime('%Y-%m-%d')}.jsonl"

    async def add_request_log(self, request_log: RequestLogObject | CallAPILogObject) -> None:
        """
        添加调用日志项

        :param request_log: 调用日志项
        :return: None
        """
        async with self._async_lock:
            # 添加日志项
            self._log_list.append(request_log)
            logger.info("Request log added", user_id=request_log.user_id)
            
            # 防抖保存操作
            if self._debonce_task and not self._debonce_task.done():
                self._debonce_task.cancel()  # 如果已有任务，先取消
            if len(self._log_list) < self._max_cache_size:
                logger.info("Request log debonce task created")
                wait_time = self._debonce_save_wait_time
            else:
                logger.info("Request log saved immediately")
                wait_time = 0
            self._debonce_task = asyncio.create_task(
                self._wait_and_save_async(
                    wait_time = wait_time
                )
            )
        
    # 将日志列表转换为字节流
    @staticmethod
    def _log_bytestream(log_list: Iterable[RequestLogObject | CallAPILogObject]) -> Generator[bytes, None, None]:
        for log in log_list:
            yield orjson.dumps(log.as_dict) + b"\n"

    def _save_request_log(self) -> None:
        """
        保存队列中的所有日志到文件
        """
        # 如果日志列表为空，直接返回
        if not self._log_list:
            return
        
        path = self.log_file_path
        
        if path.exists():
            # 如果文件存在，以追加模式打开
            with open(path, 'ab') as f:
                for chunk in self._log_bytestream(self._log_list):
                    f.write(chunk)
        else:
            # 如果文件不存在，以写入模式打开
            with open(path, 'wb') as f:
                for chunk in self._log_bytestream(self._log_list):
                    f.write(chunk)
        
        logger.info(f"Saved {len(self._log_list)} request logs to file")

        # 清空日志列表
        self._log_list.clear()

    async def _save_request_log_async(self) -> None:
        """
        异步保存队列中的所有日志到文件
        """
        # 如果日志列表为空，则直接返回
        if not self._log_list:
            return
        
        path = self.log_file_path

        if path.exists():
            # 如果文件存在，则以追加模式打开文件
            async with aiofiles.open(path, 'ab') as f:
                for chunk in self._log_bytestream(self._log_list):
                    await f.write(chunk)
        else:
            # 如果文件不存在，则以写入模式打开文件
            async with aiofiles.open(path, 'wb') as f:
                for chunk in self._log_bytestream(self._log_list):
                    await f.write(chunk)
        
        logger.info(f"Saved {len(self._log_list)} request logs to file")

        # 清空日志列表
        self._log_list.clear()

    async def read_request_log(self) -> List[RequestLogObject]:
        """
        从文件读取所有调用日志

        :return: 所有调用日志
        """
        request_log_list = []
        async for request_log in self.read_stream_request_log():
            request_log_list.append(request_log)
        return request_log_list

    async def read_stream_request_log(self) -> AsyncIterator[RequestLogObject]:
        """
        从文件流式读取所有调用日志

        :return: 读取调用日志的生成器
        """
        # 深拷贝内存日志
        async with self._async_lock:
            mem_logs = copy.deepcopy(self._log_list)
        mem_log_count = len(mem_logs)
        logger.info(f"From {mem_log_count} memory logs")

        request_log_files = np.array(
            [str(file) for file in self._base_dir.glob("*.jsonl")]
        )
        sorted_request_log_files = np.sort(request_log_files)
        
        # 读取文件日志
        readed_log_count = 0
        log_file_count = 0
        for file in sorted_request_log_files:
            path = Path(file)
            if path.exists():
                async with aiofiles.open(path, 'rb') as f:
                    async for line in f:
                        data = await asyncio.to_thread(orjson.loads, line)
                        yield RequestLogObject.from_dict(data)  # 生成文件日志
                        readed_log_count += 1  # 日志计数
                log_file_count += 1  # 文件计数
        logger.info(f"From {log_file_count} file read logs")
        
        # 输出内存日志
        for log in mem_logs:
            yield log

        # 记录总数（所有日志已生成）
        total = readed_log_count + mem_log_count
        logger.info(f"Read {total} request logs")
        
    
    def save_request_log(self) -> None:
        """
        手动保存日志到文件
        """
        # 停止防抖任务
        if self._debonce_task and not self._debonce_task.done():
            self._debonce_task.cancel()  # 如果已有任务，先取消
        self._save_request_log()
    
    async def save_request_log_async(self) -> None:
        """手动保存日志到文件"""
        async with self._async_lock:
            # 停止防抖任务
            if self._debonce_task and not self._debonce_task.done():
                self._debonce_task.cancel()  # 如果已有任务，先取消
            await self._save_request_log_async()

    async def _wait_and_save_async(self, wait_time: float = 5) -> None:
        """等待并保存日志到文件"""
        try:
            logger.info(f"Wait {wait_time} seconds to save request log")
            # 等待指定时间
            await asyncio.sleep(wait_time)
            # 时间到后保存日志
            if self._auto_save:
                await self._save_request_log_async()
            else:
                self._log_list.clear()
        except asyncio.CancelledError:
            logger.info("Request log save task cancelled")