import os
from box import Box
import yaml
import orjson
from typing import Generator, Iterable
from pathlib import Path
from ._base_model import Base_Config

class ConfigLoader:
    def __init__(self, config_dir: str | os.PathLike = "./config"):
        self._config_dir = Path(config_dir)
    
    def _scan_dir(self, globs: Iterable[str]) -> Generator[Path, None, None]:
        for glob in globs:
            for path in self._config_dir.glob(glob):
                yield path
    
    def _config_files(self) -> list[Path]:
        return sorted(
            self._scan_dir(
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
    
    def load(self) -> Base_Config:
        configs: list[Box] = []
        for path in self._config_files():
            if path.suffix in [".yaml", ".yml"]:
                configs.append(Box(self._load_yaml(path)))
            elif path.suffix == ".json":
                configs.append(Box(self._load_json(path)))
        
        if not configs:
            return {}
        
        base_config = configs[0]
        for config in configs[1:]:
            base_config.merge_update(config)
        
        return Base_Config(**base_config.to_dict())
