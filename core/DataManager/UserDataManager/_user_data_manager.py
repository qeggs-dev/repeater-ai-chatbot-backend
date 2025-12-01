from ConfigManager import ConfigLoader
from ._main_user_data_manager import MainManager as UserDataManager
from typing import Any

configs = ConfigLoader()

_sub_dir_name:str = configs.get_config("user_data.sub_dir_name", "ParallelData").get_value(str)
_cache_metadata:bool = configs.get_config("user_data.cache_metadata", False).get_value(bool)
_cache_data:bool = configs.get_config("user_data.cache_data", False).get_value(bool)


class _baseManager(UserDataManager):
    def __init__(self, base_name: str):
        self.base_name = base_name if base_name else "UserData"
        super().__init__(
            base_name = self.base_name,
            cache_metadata = configs.get_config(f"user_data.{self.base_name}.cache_metadata", _cache_metadata).get_value(bool),
            cache_data = configs.get_config(f"user_data.{self.base_name}.cache_data", _cache_data).get_value(bool),
            sub_dir_name = _sub_dir_name
        )

class ContextManager(_baseManager):
    def __init__(self):
        super().__init__('Context_UserData')
    
    async def load(self, user_id: str, default: list = []):
        return await super().load(user_id, default if isinstance(default, list) else [])
    
    async def save(self, user_id: str, data: list):
        await super().save(user_id, data if isinstance(data, list) else [])

class PromptManager(_baseManager):
    def __init__(self):
        super().__init__('Prompt_UserData')
    
    async def load(self, user_id: str, default: str = ""):
        return await super().load(user_id, default if isinstance(default, str) else "")
    
    async def save(self, user_id: str, data: str):
        await super().save(user_id, data if isinstance(data, str) else "")

class UserConfigManager(_baseManager):
    def __init__(self):
        super().__init__('UserConfig_UserData')
    
    async def load(self, user_id: str, default: dict = {}):
        return await super().load(user_id, default if isinstance(default, dict) else {})
    
    async def save(self, user_id: str, data: dict):
        await super().save(user_id, data if isinstance(data, dict) else {})