
from ._main_user_data_manager import MainManager as UserDataManager
from typing import Any
from ...Global_Config_Manager import configs, Change_Data_Config

class ContextManager(UserDataManager):
    def __init__(self):
        super().__init__(
            "Context_UserData",
            cache_metadata = (
                configs.user_data.cache_medadata.context
                if isinstance(configs.user_data.cache_medadata, Change_Data_Config)
                else configs.user_data.cache_medadata
            ),
            cache_data = (
                configs.user_data.cache_data.context
                if isinstance(configs.user_data.cache_data, Change_Data_Config)
                else configs.user_data.cache_data
            ),
            branches_dir_name = configs.user_data.branches_dir_name
        )
    
    async def load(self, user_id: str, default: list = []):
        return await super().load(user_id, default if isinstance(default, list) else [])
    
    async def save(self, user_id: str, data: list):
        await super().save(user_id, data if isinstance(data, list) else [])

class PromptManager(UserDataManager):
    def __init__(self):
        super().__init__(
            "Prompt_UserData",
            cache_metadata = (
                configs.user_data.cache_medadata.prompt
                if isinstance(configs.user_data.cache_medadata, Change_Data_Config)
                else configs.user_data.cache_medadata
            ),
            cache_data = (
                configs.user_data.cache_data.prompt
                if isinstance(configs.user_data.cache_data, Change_Data_Config)
                else configs.user_data.cache_data
            ),
            branches_dir_name = configs.user_data.branches_dir_name
        )
    
    async def load(self, user_id: str, default: str = ""):
        return await super().load(user_id, default if isinstance(default, str) else "")
    
    async def save(self, user_id: str, data: str):
        await super().save(user_id, data if isinstance(data, str) else "")

class UserConfigManager(UserDataManager):
    def __init__(self):
        super().__init__(
            "UserConfig_UserData",
            cache_metadata = (
                configs.user_data.cache_medadata.config
                if isinstance(configs.user_data.cache_medadata, Change_Data_Config)
                else configs.user_data.cache_medadata
            ),
            cache_data = (
                configs.user_data.cache_data.config
                if isinstance(configs.user_data.cache_data, Change_Data_Config)
                else configs.user_data.cache_data
            ),
            branches_dir_name = configs.user_data.branches_dir_name
        )
    
    async def load(self, user_id: str, default: dict = {}):
        return await super().load(user_id, default if isinstance(default, dict) else {})
    
    async def save(self, user_id: str, data: dict):
        await super().save(user_id, data if isinstance(data, dict) else {})