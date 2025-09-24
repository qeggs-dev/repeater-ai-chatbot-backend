# ==== 标准库 ==== #
from typing import Any
from pathlib import Path

# ==== 第三方库 ==== #
from loguru import logger

# ==== 自定义库 ==== #
from .SubManager import SubManager
from PathProcessors import validate_path, sanitize_filename, sanitize_filename_async
from ConfigManager import ConfigLoader
from ._user_mainmanager_interface import UserMainManagerInterface

configs = ConfigLoader()

class MainManager(UserMainManagerInterface):
    def __init__(self, base_name: str, cache_metadata:bool = False, cache_data:bool = False, sub_dir_name:str = "ParallelData"):
        self._base_path = configs.get_config("User_Data.Dir", "./data/userdata").get_value(Path)
        self._base_name = sanitize_filename(base_name)
        if not validate_path(self._base_path, self._base_name):
            raise ValueError("Invalid path for user data directory")
        self.sub_managers:dict[str, SubManager] = {}

        self.cache_metadata = cache_metadata
        self.cache_data = cache_data

        self.sub_dir_name = sub_dir_name
    
    @property
    def base_path(self):
        return self._base_path / self._base_name
    
    async def load(self, user_id: str, default: Any = None) -> Any:
        user_id = await sanitize_filename_async(user_id)
        manager = self.sub_managers.setdefault(
            user_id,
            SubManager(
                self.base_path / user_id,
                sub_dir_name = self.sub_dir_name,
                cache_metadata = self.cache_metadata,
                cache_data = self.cache_data
            )
        )
        try:
            metadata = await manager.load_metadata()
        except FileNotFoundError:
            logger.error(f"Read User Metadata File Does Not Exist", user_id = user_id)
            raise
        except PermissionError:
            logger.error(f"Read User Metadata File Permission Denied", user_id = user_id)
            raise
        except IsADirectoryError:
            logger.error(f"Read User Metadata File Is A Directory", user_id = user_id)
            raise
        except OSError as e:
            logger.error(f"Read User Metadata File Other OS Error: {e}", user_id = user_id)
            raise
        
        if isinstance(metadata, dict):
            item = metadata.get('default_item', 'default')
        else:
            item = 'default'
        
        try:
            return await manager.load(item, default)
        except FileNotFoundError:
            logger.error(f"Read User File Does Not Exist", user_id = user_id)
            raise
        except PermissionError:
            logger.error(f"Read User File Permission Denied", user_id = user_id)
            raise
        except IsADirectoryError:
            logger.error(f"Read User File Is A Directory", user_id = user_id)
            raise
        except OSError as e:
            logger.error(f"Read User File Other OS Error: {e}", user_id = user_id)
            raise
    
    async def save(self, user_id: str, data: Any) -> None:
        user_id = await sanitize_filename_async(user_id)
        manager = self.sub_managers.setdefault(
            user_id,
            SubManager(
                self.base_path / user_id,
                sub_dir_name = self.sub_dir_name,
                cache_metadata = self.cache_metadata,
                cache_data = self.cache_data
            )
        )
        try:
            metadata = await manager.load_metadata()
        except FileNotFoundError:
            logger.error(f"Read User Metadata File Does Not Exist", user_id = user_id)
            raise
        except PermissionError:
            logger.error(f"Read User Metadata File Permission Denied", user_id = user_id)
            raise
        except IsADirectoryError:
            logger.error(f"Read User Metadata File Is A Directory", user_id = user_id)
            raise
        except OSError as e:
            logger.error(f"Read User Metadata File Other OS Error: {e}", user_id = user_id)
            raise

        if isinstance(metadata, dict):
            item = metadata.get('default_item', 'default')
        else:
            item = 'default'
        try:
            await manager.save(item, data)
        except PermissionError:
            logger.error(f"Write User File Permission Denied", user_id = user_id)
            raise
        except IsADirectoryError:
            logger.error(f"Write User File Is A Directory", user_id = user_id)
            raise
        except OSError as e:
            logger.error(f"Write User File Other OS Error: {e}", user_id = user_id)
            raise
    
    async def delete(self, user_id: str) -> None:
        user_id = await sanitize_filename_async(user_id)
        manager = self.sub_managers.setdefault(
            user_id,
            SubManager(
                self.base_path / user_id,
                sub_dir_name = self.sub_dir_name,
                cache_metadata = self.cache_metadata,
                cache_data=self.cache_data
            )
        )

        try:
            metadata = await manager.load_metadata()
        except FileNotFoundError:
            logger.error(f"Read User Metadata File Not Found")
            raise
        except PermissionError:
            logger.error(f"Read User Metadata File Permission Denied", user_id = user_id)
            raise
        except IsADirectoryError:
            logger.error(f"Read User Metadata File Is A Directory", user_id = user_id)
            raise
        except OSError as e:
            logger.error(f"Read User Metadata File Other OS Error: {e}", user_id = user_id)
            raise

        if isinstance(metadata, dict):
            item = metadata.get('default_item', 'default')
        else:
            item = 'default'
        try:
            await manager.delete(item)
        except PermissionError:
            logger.error(f"Delete User File Permission Denied", user_id = user_id)
            raise
        except IsADirectoryError:
            logger.error(f"Delete User File Is A Directory", user_id = user_id)
            raise
        except OSError as e:
            logger.error(f"Delete User File Other OS Error: {e}", user_id = user_id)
            raise
    
    async def set_default_item_id(self, user_id: str, item: str) -> None:
        user_id = await sanitize_filename_async(user_id)
        manager = self.sub_managers.setdefault(
            user_id,
            SubManager(
                self.base_path / user_id,
                sub_dir_name = self.sub_dir_name,
                cache_metadata = self.cache_metadata,
                cache_data = self.cache_data
            )
        )

        try:
            metadata = await manager.load_metadata()
        except FileExistsError:
            logger.error(f"Read User Metadata File Not Found", user_id = user_id)
            raise
        except PermissionError:
            logger.error(f"Read User Metadata File Permission Denied", user_id = user_id)
            raise
        except IsADirectoryError:
            logger.error(f"Read User Metadata File Is A Directory", user_id = user_id)
            raise
        except OSError as e:
            logger.error(f"Read User Metadata File Other OS Error: {e}", user_id = user_id)
            raise

        if isinstance(metadata, dict):
            metadata['default_item'] = item
        else:
            metadata = {'default_item': item}
        try:
            await manager.save_metadata(metadata)
        except PermissionError:
            logger.error(f"Write User Metadata File Permission Denied", user_id = user_id)
            raise
        except IsADirectoryError:
            logger.error(f"Write User Metadata File Is A Directory", user_id = user_id)
            raise
        except OSError as e:
            logger.error(f"Write User Metadata File Other OS Error: {e}", user_id = user_id)
            raise

    async def get_default_item_id(self, user_id: str) -> str:
        user_id = await sanitize_filename_async(user_id)
        manager = self.sub_managers.setdefault(
            user_id,
            SubManager(
                self.base_path / user_id,
                sub_dir_name = self.sub_dir_name,
                cache_metadata = self.cache_metadata,
                cache_data = self.cache_data
            )
        )
        try:
            metadata = await manager.load_metadata()
        except FileExistsError:
            logger.error(f"Read User Metadata File Not Found", user_id = user_id)
            raise
        except PermissionError:
            logger.error(f"Read User Metadata File Permission Denied", user_id = user_id)
            raise
        except IsADirectoryError:
            logger.error(f"Read User Metadata File Is A Directory", user_id = user_id)
            raise
        except OSError as e:
            logger.error(f"Read User Metadata File Other OS Error: {e}", user_id = user_id)
            raise
        if isinstance(metadata, dict):
            return metadata.get('default_item', 'default')
        else:
            return 'default'

    async def get_all_user_id(self) -> list:
        return [f.name for f in (self.base_path).iterdir() if f.is_dir()]

    async def get_all_item_id(self, user_id: str) -> list:
        return [f.stem for f in (self.base_path / user_id / self.sub_dir_name).iterdir() if f.is_file()]