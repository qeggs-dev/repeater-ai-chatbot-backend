import os
from ._loader import ConfigLoader
from ._base_model import Base_Config

def get_config(config_dir: str | os.PathLike) -> Base_Config:
    loader = ConfigLoader(config_dir)
    return loader.load()