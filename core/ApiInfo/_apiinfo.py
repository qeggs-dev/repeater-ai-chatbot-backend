import re
import asyncio
import aiofiles
from pathlib import Path
from typing import Dict, List
from loguru import logger

from ._pydantic_models import ApiInfoConfig, ApiGroup
from ._api_obj import ApiObject
from ._exceptions import *

class ApiInfo:
    def __init__(self, case_sensitive: bool = False):
        self._api_objs: dict[str, list[ApiObject]] = {}
        self._case_sensitive: bool = case_sensitive

    def _create_api_group(self, api_data: list[dict]) -> ApiGroup:
        """Create an ApiGroup instance from raw data."""
        return ApiGroup(api = api_data)

    def _parse_api_groups(self, raw_api_groups: list[dict]) -> None:
        """Parse raw API groups data and populate indexes."""
        if not isinstance(raw_api_groups, list):
            raise ValueError('api_groups must be a list')
        
        api_groups: ApiGroup = self._create_api_group(raw_api_groups)
        self._api_groups = api_groups
        for group in api_groups.api:
            for model in group.models:
                api_obj = ApiObject(
                    name = model.name,
                    uid = model.uid,
                    id = model.id,
                    api_key_env = group.api_key_env,
                    parent = group.name,
                    url = model.url or group.url,
                    type = model.type,
                    timeout = model.timeout or group.timeout or 60.0,
                )
                if api_obj.uid not in self._api_objs:
                    self._api_objs[api_obj.uid] = [api_obj]
                else:
                    self._api_objs[api_obj.uid].append(api_obj)


    def load(self, path: Path) -> None:
        """Load and parse API groups from a JSON/YAML file."""
        if not path.exists():
            raise FileNotFoundError(f"File '{path}' does not exist")
        
        if path.suffix.lower() == '.json':
            import orjson
            try:
                with open(path, 'rb') as f:
                    fdata = f.read()
                    raw_api_groups: list[dict] = orjson.loads(fdata)
                    self._parse_api_groups(raw_api_groups)
            except orjson.JSONDecodeError as e:
                raise ValueError(f'Invalid JSON format: {e}')
            except OSError as e:
                raise IOError(f'Failed to read file: {e}')
        elif path.suffix.lower() == '.yaml' or path.suffix.lower() == '.yml':
            import yaml
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    fdata = f.read()
                    raw_api_groups: list[dict] = yaml.safe_load(fdata)
                    self._parse_api_groups(raw_api_groups)
            except yaml.YAMLError as e:
                raise ValueError(f'Invalid YAML format: {e}')
            except OSError as e:
                raise IOError(f'Failed to read file: {e}')
        else:
            raise ValueError(f'Invalid file format: {path.suffix}')

    async def load_async(self, path: Path) -> None:
        """Load and parse API groups from a JSON/YAML file."""
        if not path.exists():
            raise FileNotFoundError(f"File '{path}' does not exist")
        
        if not path.suffix.lower() == '.json':
            import orjson
            try:
                async with aiofiles.open(path, 'rb') as f:
                    fdata = await f.read()
                    raw_api_groups: list[dict] = orjson.loads(fdata)
                    self._parse_api_groups(raw_api_groups)
            except orjson.JSONDecodeError as e:
                raise ValueError(f'Invalid JSON format: {e}')
            except OSError as e:
                raise IOError(f'Failed to read file: {e}')
        elif path.suffix.lower() == '.yaml' or path.suffix.lower() == '.yml':
            import yaml
            try:
                async with aiofiles.open(path, 'r', encoding='utf-8') as f:
                    fdata = await f.read()
                    raw_api_groups: list[dict] = yaml.safe_load(fdata)
                    self._parse_api_groups(raw_api_groups)
            except yaml.YAMLError as e:
                raise ValueError(f'Invalid YAML format: {e}')
            except OSError as e:
                raise IOError(f'Failed to read file: {e}')
        else:
            raise ValueError(f'Invalid file format: {path.suffix}')

    def find(self, model_uid: str, default: list[ApiObject] | None = None) -> list[ApiObject]:
        """Find API groups by model uid."""
        if self._case_sensitive:
            key = model_uid
        else:
            key = model_uid.lower()

        index_list = self._api_objs.get(key, default)
        if index_list is None:
            return []
        
        return index_list.copy()