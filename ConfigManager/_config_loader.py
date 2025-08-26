import asyncio
import aiofiles
import threading
from ._config_object import ConfigObject
from ._config_data_model import Config_Model
from ._exceptions import *
from typing import Any
from loguru import logger
import platform
from pydantic import ValidationError
from pathlib import Path
from environs import Env

env = Env()

class ConfigLoader:
    """
    This class is used to automatically manage configuration information for the entire project.
    """
    _golbal_config: dict[str, ConfigObject] = {}

    def __init__(
            self,
            config_file_path: str | Path | None = None,
            strictly_case_sensitive: bool = False,
            use_global: bool = True
        ):
        self._use_global = use_global
        self._config: dict[str, ConfigObject] = {}
        self._config_sync_lock = threading.Lock()
        self._config_async_lock = asyncio.Lock()
        self._config_environment = env.str("CONFIG_ENVIRONMENT", "")

        self._strictly_case_sensitive = strictly_case_sensitive

        if config_file_path is not None:
            self._config_file_path = Path(config_file_path)
            self.load_config(config_file_path)
        else:
            self._config_file_path = None
    
    @property
    def _get_config(self) -> dict[str, ConfigObject]:
        if self._use_global:
            return self._golbal_config
        return self._config
    
    def __repr__(self) -> str:
        return f"<ConfigLoader Length={len(self._get_config)}>"

    async def load_config_async(self, file_path: str | Path):
        """
        This method is used to load configuration information from a file.

        :param file_path: The file path of the configuration file.
        :return: None
        """
        async with self._config_async_lock:
            async with aiofiles.open(file_path, mode='rb') as f:
                config = await f.read()
            config:list[dict[str, Any]] = self._loads_data(config, Path(file_path).suffix)
            await asyncio.to_thread(self._decode_config, config)
    
    async def reload_config_async(self):
        """
        This method is used to reload configuration information.
        """
        if self._config_file_path is not None:
            await self.load_config_async(self._config_file_path)
    
    def load_config(self, file_path: str | Path):
        """
        This method is used to load configuration information from a file.

        :param file_path: The file path of the configuration file.
        :return: None
        """
        import orjson
        with self._config_sync_lock:
            with open(file_path, mode='rb') as f:
                config = f.read()
            
            config:list[dict[str, Any]] = self._loads_data(config, Path(file_path).suffix)
            self._decode_config(config)
    
    def reload_config(self):
        """
        This method is used to reload configuration information.
        """
        if self._config_file_path is not None:
            self.load_config(self._config_file_path)
    
    def _loads_data(self, load_data: str, expand_name: str):
        """
        This method is used to load data from a file.

        :param load_data: The data to be loaded.
        :param expand_name: The file extension name.
        :return: None
        """
        if expand_name == '.json':
            import orjson
            try:
                config_data = orjson.loads(load_data)
            except orjson.JSONDecodeError:
                raise ConfigFileLoadError("Failed to load JSON file.")
        elif expand_name in {'.yaml', '.yml'}:
            import yaml
            try:
                config_data = yaml.safe_load(load_data)
            except yaml.YAMLError:
                raise ConfigFileLoadError("Failed to load YAML file.")
        else:
            raise ValueError(f'Unsupported file extension: {expand_name}')
        return config_data

        
    def _decode_config(self, config_list: list[dict[str, Any]]):
        """
        This method is used to decode the configuration information.

        :return: The decoded configuration information.
        """
        if not isinstance(config_list, list):
            raise TypeError("Config must be a list.")
        system = platform.system().lower()
        configs = self._get_config
        import orjson
        import yaml
        for item in reversed(config_list):
            try:
                config_model = Config_Model(**item)
            except ValidationError as e:
                raise ConfigSyntaxError("Invalid config syntax.", e.errors())
            if self._strictly_case_sensitive:
                name = config_model.name
            else:
                name = config_model.name.lower()
            if name in configs:
                config = configs[name]
            else:
                config = ConfigObject(name = name)

            for value_item in reversed(config_model.values):
                if (
                    (
                        # If environment is None, it means it's a global value
                        value_item.environment is None or
                        # If environment is set, it must match the current environment
                        (value_item.environment == self._config_environment)
                    ) and (
                        # If system is None, "all", "*", it means it's a global value
                        (value_item.system.lower() if value_item.system else None) in {system, "*", "all", None}
                    )
                ):
                    type = value_item.type
                    TYPES = {
                        "int": int,
                        "float": float,
                        "str": str,
                        "list": list,
                        "dict": dict
                    }
                    try:
                        if value_item.value is None:
                            value = None
                        if type in TYPES:
                            value = TYPES[type](value_item.value)
                        elif type == "bool":
                            if isinstance(value_item.value, str):
                                value = value_item.value.lower() in {"true", "1", "yes"}
                            else:
                                value = bool(value_item.value)
                        elif type == "json":
                            value = orjson.loads(value_item.value)
                        elif type == "yaml":
                            value = yaml.load(value_item.value)
                        elif type == "path":
                            value = Path(value_item.value)
                        elif type in {"auto", "other"}:
                            value = value_item.value
                        config.value = value
                    except (ValueError, TypeError, orjson.JSONDecodeError, yaml.YAMLError):
                        logger.warning(f"The custom configuration data type conversion failed, and an attempt has been made to use the {config.value_type} type.")
                        config.value = value_item.value
            
            configs[name] = config
    
    def __getitem__(self, name: str) -> ConfigObject:
        configs = self._get_config()
        if name not in configs:
            raise KeyError(f"The configuration item '{name}' does not exist.")
        return configs[name]

    def get_config(self, name: str, default: Any = None) -> ConfigObject:
        configs = self._get_config
        if not self._strictly_case_sensitive:
            name = name.lower()
        if name in configs:
            return configs[name]
        else:
            config = ConfigObject(name = name)
            config.value = default
            return config

    def get_configs(self, names: list[str]) -> dict[str, ConfigObject]:
        return {name: self.get_config(name) for name in names}
    
    def add_config(self, name: str, value: Any) -> None:
        configs = self._get_config
        if not self._strictly_case_sensitive:
            name = name.lower()
        
        if name in configs:
            config = configs[name]
        else:
            config = ConfigObject(name)
        config.value = value

        configs[name] = config
    
    def seek_config(self, name: str, index: int) -> bool:
        """
        Seek to a specific index.

        :param index: The index to seek to.
        """
        config = self._get_config
        if name in config:
            return config[name].seek(index)
        return False
    
    def forwardtracking_config(self, name: str, offset: int = 1) -> bool:
        """
        Forward tracking.

        :param offset: The offset to forward tracking.
        """
        config = self._get_config
        if name in config:
            return config[name].forwardtracking(offset)
        return False
    
    def __contains__(self, name: str) -> bool:
        return name in self._get_config