from __future__ import annotations
import os
from box import Box
import yaml
import orjson
from typing import Generator, Iterable
from pathlib import Path
from ._base_model import Base_Config
import shutil

configs = Base_Config()

class ConfigLoader:
    _instance: ConfigLoader | None = None
    _base_path: Path

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.load()
        return cls._instance

    @classmethod
    def update_base_path(cls, path: str | os.PathLike) -> None:
        cls._base_path = Path(path)
    
    @classmethod
    def _scan_dir(cls, globs: Iterable[str]) -> Generator[Path, None, None]:
        for glob in globs:
            for path in cls._base_path.glob(glob):
                yield path
    
    @classmethod
    def _config_files(cls) -> list[Path]:
        return sorted(
            cls._scan_dir(
                [
                    "*.yaml",
                    "*.yml",
                    "*.json",
                ]
            ),
            key=lambda path: path.name
        )
    
    @staticmethod
    def _load_yaml(path: Path) -> dict:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    
    @staticmethod
    def _load_json(path: Path) -> dict:
        with open(path, "rb") as f:
            return orjson.loads(f.read())
    
    @classmethod
    def load(cls, write_when_it_fails: bool = False) -> Base_Config:
        """
        Load the configs from the config files.

        :param use_cache: If True, use the cached config, otherwise reload the config
        """
        try:
            configs: list[Box] = []
            for path in cls._config_files():
                if path.suffix in [".yaml", ".yml"]:
                    configs.append(Box(cls._load_yaml(path)))
                elif path.suffix == ".json":
                    configs.append(Box(cls._load_json(path)))
            
            if not configs:
                return {}
            
            base_config = configs[0]
            for config in configs[1:]:
                base_config.merge_update(config)
            
            return Base_Config(**base_config.to_dict())
        except Exception as e:
            if write_when_it_fails:
                cls.save(config)
            else:
                raise
    
    @staticmethod
    def update_config(config: Base_Config) -> None:
        global configs
        configs = config
    
    @staticmethod
    def _dump_yaml(path: Path, data: Base_Config) -> None:
        with open(path, "w", encoding="utf-8") as f:
            f.write(
                yaml.safe_dump(
                    data.model_dump(),
                    allow_unicode=True,
                    sort_keys=False
                )
            )
    
    @staticmethod
    def _dump_json(path: Path, data: Base_Config) -> None:
        with open(path, "wb") as f:
            f.write(
                orjson.dumps(
                    data.model_dump()
                )
            )
    
    @classmethod
    def save(cls, config: Base_Config, filename: str = "config.json") -> None:
        """
        Save the config to the config files.
        
        :param config: The config to save
        """
        shutil.rmtree(cls._base_path)
        cls._base_path.mkdir(parents=True, exist_ok=True)
        config_file_path = cls._base_path / filename
        if config_file_path.suffix in [".yaml", ".yml"]:
            cls._dump_yaml(config_file_path, config)
        elif config_file_path.suffix == ".json":
            cls._dump_json(config_file_path, config)
            