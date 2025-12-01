import asyncio
from typing import Any
from loguru import logger
from ..Data_Manager import UserConfigManager
from ._exceptions import *
from ._object import Configs
from ..Global_Config_Manager import configs

class ConfigManager:
    # 用户配置管理器 (定义为类属性以减少重复实例化)
    _user_config_manager = UserConfigManager()

    # 全局配置缓存
    _global_config_cache:dict[str, Configs] = {}
    
    def __init__(
            self,
            cache: bool = True,
            use_global_cache: bool = False,
            downgrade_wait_time: float | None = None,
            debonce_save_wait_time: float | None = None
        ):
        self._cache:dict[str, Configs] = {}

        self._cache_switch = cache
        self._use_global_cache = use_global_cache

        self._downgrade_tasks: dict[str, asyncio.Task] = {}
        self._downgrade_wait_time: float = downgrade_wait_time or configs.user_config_cache.downgrade_wait_time

        self._debonce_save_tasks: dict[str, asyncio.Task] = {}
        self._debonce_save_wait_time: float = debonce_save_wait_time or configs.user_config_cache.debounce_save_wait_time

        self._lock = asyncio.Lock()

    async def _get_cache(self):
        if self._use_global_cache:
            return self._global_config_cache
        else:
            return self._cache
    
    async def load(self, user_id: str) -> Configs:
        """
        获取用户配置
        
        :param user_id: 用户ID
        :return: 用户配置
        """
        cache = await self._get_cache()

        if self._cache_switch:
            async with self._lock:
                if user_id in cache:
                    logger.info("Get config form cache", user_id = user_id)
                    config = cache[user_id]
                else:
                    config = Configs(
                        user_id = user_id,
                        configs = await self._user_config_manager.load(user_id)
                    )
                    cache[user_id] = config
                    logger.info("Get config from database and save to cache", user_id = user_id)
                
                # 如果已有任务，先取消
                if user_id in self._downgrade_tasks and not self._downgrade_tasks[user_id].done():
                    self._downgrade_tasks[user_id].cancel()
                task = asyncio.create_task(
                    self._wait_and_downgrade(user_id=user_id, wait_time=self._downgrade_wait_time)
                )
                logger.info(f"Create downgrade task", user_id = user_id)
                # 任务完成自动删除
                task.add_done_callback(lambda _, id=user_id: self._downgrade_tasks.pop(id, None))
                self._downgrade_tasks[user_id] = task
            return config
        else:
            logger.info("Get config from database", user_id = user_id)
            return Configs(
                user_id = user_id,
                configs = await self._user_config_manager.load(user_id)
            )
    
    async def save(self, user_id: str, configs: Configs) -> None:
        """
        保存用户配置

        :param user_id: 用户ID
        :param configs: 用户配置
        :return: None
        """
        cache = await self._get_cache()

        if self._cache_switch:
            if user_id in cache:
                if isinstance(configs, Configs):
                    async with self._lock:
                        logger.info("Save config to cache", user_id = user_id)
                        cache[user_id] = configs

                        if user_id in cache and (user_id in self._debonce_save_tasks and not self._debonce_save_tasks[user_id].done()):
                            self._debonce_save_tasks[user_id].cancel()
                        task = asyncio.create_task(
                            self._wait_and_save(user_id, self._debonce_save_wait_time)
                        )
                        logger.info(f"Create save task", user_id = user_id)
                        task.add_done_callback(lambda _, id=user_id: self._debonce_save_tasks.pop(id, None))
                        self._debonce_save_tasks[user_id] = task
                else:
                    raise TypeError("configs must be Configs object")
        else:
            logger.info("Save config to database", user_id = user_id)
            await self._user_config_manager.save(user_id, configs.configs)
    
    async def _wait_and_downgrade(self, user_id: str, wait_time: float = 5) -> None:
        """
        等待并降级用户配置

        :param user_id: 用户ID
        :return: None
        """
        try:
            await asyncio.sleep(wait_time)
            async with self._lock:
                if user_id in self._debonce_save_tasks and not self._debonce_save_tasks[user_id].done():
                    logger.warning("User config Save task is running, downgrade config cancelled", user_id = user_id)
                    return
                cache = await self._get_cache()
                if user_id in cache:
                    logger.info("Downgrade config", user_id = user_id)
                    del cache[user_id]
        except asyncio.CancelledError:
            logger.info("User config downgrade task cancelled", user_id = user_id)
    
    async def _wait_and_save(self, user_id: str, wait_time: float = 5) -> None:
        """
        等待并保存用户配置

        :param user_id: 用户ID
        :return: None
        """
        try:
            await asyncio.sleep(wait_time)
            async with self._lock:
                cache = await self._get_cache()
                if user_id in cache:
                    logger.info("Save config", user_id = user_id)
                    await self._user_config_manager.save(user_id, cache[user_id].configs)
                    del cache[user_id]
        except asyncio.CancelledError:
            logger.info("User config save task cancelled", user_id = user_id)
     
    async def get_default_item(self, user_id: str) -> str:
        """
        获取默认配置项

        :param user_id: 用户ID
        :param item: 配置项
        :return: 配置项
        """
        async with self._lock:
            return await self._user_config_manager.get_default_item_id(user_id)
    
    async def set_default_item(self, user_id: str, item: str) -> None:
        """
        设置默认配置项

        :param user_id: 用户ID
        :param item: 配置项
        :return: None
        """
        async with self._lock:
            await self._user_config_manager.set_default_item_id(user_id, item)
            logger.info("Set default config item", user_id = user_id, item = item)
    
    async def delete(self, user_id: str) -> None:
        """
        删除用户配置

        :param user_id: 用户ID
        :return: None
        """
        async with self._lock:
            cache = await self._get_cache()
            if user_id in cache:
                del cache[user_id]
            await self._user_config_manager.delete(user_id)
            logger.info("Delete config", user_id = user_id)
    
    async def clear_cache(self) -> None:
        """
        清除缓存
        """
        (await self._get_cache()).clear()
        
    async def force_write(self, user_id: str, configs: Configs) -> None:
        """
        强制写入配置

        :param user_id: 用户ID
        :param configs: 用户配置
        :return: None
        """
        async with self._lock:
            cache = await self._get_cache()
            await self._user_config_manager.save(user_id, configs.configs)
            cache[user_id] = configs
            logger.info("Force write config", user_id = user_id)

    async def save_all(self, clear_all_tasks: bool = True) -> None:
        """
        保存所有用户配置

        :return: None
        """
        async with self._lock:
            cache = await self._get_cache()

            for user_id, configs in cache.items():
                await self._user_config_manager.save(user_id, configs.configs)
                if clear_all_tasks:
                    self._downgrade_tasks[user_id].cancel()
                    self._debonce_save_tasks[user_id].cancel()
            logger.info(f"Saved {len(cache)} config", user_id = user_id)
            cache.clear()
    
    async def get_all(self):
        """
        获取所有用户配置

        :param cache: 缓存字典
        :return: 所有用户的配置数据
        """
        async with self._lock:
            cache = await self._get_cache()

            userlist = await self._user_config_manager.get_all_user_id()
            for user_id in userlist:
                cache[user_id] = Configs(
                    user_id = user_id,
                    configs = await self._user_config_manager.load(user_id)
                )
            logger.info(f"Loaded {len(cache)} configs")
            return cache
    
    async def get_all_user_id(self):
        """
        获取所有用户ID

        :return: 所有用户ID
        """
        return await self._user_config_manager.get_all_user_id()
    
    async def get_all_item_id(self):
        """
        获取所有配置ID

        :return: 配置项ID列表
        """
        return await self._user_config_manager.get_all_item_id()
    
    async def __aenter__(self):
        return self 

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.save_all()