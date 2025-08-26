import re
import asyncio
import aiofiles
from pathlib import Path
from typing import Dict, List, Optional, Union

from ._apigroup import ApiGroup
from ._exceptions import *

class ApiInfo:
    def __init__(self, CaseSensitive: bool = False):
        self._api_groups: List[ApiGroup] = []
        self._api_uids: Dict[str, List[int]] = {}
        self._api_names: Dict[str, List[int]] = {}
        self._api_base_groups: Dict[str, List[int]] = {}
        self._api_task_types: Dict[str, List[int]] = {}
        self.CaseSensitive = CaseSensitive
        self._filter_expression_parser = re.compile(r"(?P<findmode>uid|name|base_group|task_type)\s*=\s*(?P<value>.*)")

    def _create_api_group(self, api_data: dict, model_data: dict) -> ApiGroup:
        """Create an ApiGroup instance from raw data."""
        metadata:dict = api_data.get('Metadata', {})
        if 'Metadata' in model_data:
            metadata.update(model_data.get('Metadata', {}))
        
        request_type = model_data.get('request_type', 'GET')
        if request_type not in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
            request_type = "GET"
        
        return ApiGroup(
            group_name = api_data.get('Name', ''),
            api_key_envname = model_data.get('ApiKeyEnv', api_data.get('ApiKeyEnv', '')),
            model_name = model_data.get('Name', ''),
            url = model_data.get('URL', api_data.get('URL', '')),
            request_type = request_type,
            model_id = model_data.get('Id', ''),
            model_uid = model_data.get('Uid', ''),
            task_type = model_data.get('TaskType', ''),
            metadata = metadata,
        )

    def _add_api_group(self, api_group: ApiGroup) -> None:
        """Add an ApiGroup to all relevant indexes."""
        self._api_groups.append(api_group)
            
        # Update type index
        if self.CaseSensitive:
            model_uid_key = api_group.model_uid
            model_name_key = api_group.model_name
            group_name_key = api_group.group_name
            task_type_key = api_group.task_type
        else:
            model_uid_key = api_group.model_uid.lower()
            model_name_key = api_group.model_name.lower()
            group_name_key = api_group.group_name.lower()
            task_type_key = api_group.task_type.lower()
        
        self._api_uids.setdefault(model_uid_key, []).append(len(self._api_groups) - 1)
        self._api_names.setdefault(model_name_key, []).append(len(self._api_groups) - 1)
        self._api_base_groups.setdefault(group_name_key, []).append(len(self._api_groups) - 1)
        self._api_task_types.setdefault(task_type_key, []).append(len(self._api_groups) - 1)

    def _parse_api_groups(self, raw_api_groups: List[dict]) -> None:
        """Parse raw API groups data and populate indexes."""
        if not isinstance(raw_api_groups, list):
            raise ValueError('api_groups must be a list')
            
        for api_data in raw_api_groups:
            if not isinstance(api_data, dict):
                raise ValueError('Each API group must be a dictionary')
                
            models = api_data.get('models', [])
            if not isinstance(models, list):
                raise ValueError('models must be a list')
                
            for model_data in models:
                if not isinstance(model_data, dict):
                    raise ValueError('Each model must be a dictionary')
                    
                api_group = self._create_api_group(api_data, model_data)
                self._add_api_group(api_group)
    
    def load(self, path: Path) -> None:
        """Load and parse API groups from a JSON/YAML file."""
        if not path.exists():
            raise FileNotFoundError(f"File '{path}' does not exist")
        
        if path.suffix.lower() == '.json':
            import orjson
            try:
                with open(path, 'rb') as f:
                    fdata = f.read()
                    raw_api_groups: List[dict] = orjson.loads(fdata)
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
                    raw_api_groups: List[dict] = yaml.safe_load(fdata)
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
                    raw_api_groups: List[dict] = orjson.loads(fdata)
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
                    raw_api_groups: List[dict] = yaml.safe_load(fdata)
                    self._parse_api_groups(raw_api_groups)
            except yaml.YAMLError as e:
                raise ValueError(f'Invalid YAML format: {e}')
            except OSError as e:
                raise IOError(f'Failed to read file: {e}')
        else:
            raise ValueError(f'Invalid file format: {path.suffix}')

    def find_uid(self, model_uid: str, default: list[ApiGroup] = None) -> List[ApiGroup]:
        """Find API groups by model uid."""
        if self.CaseSensitive:
            key = model_uid
        else:
            key = model_uid.lower()

        index_list = self._api_uids.get(key, None)
        if index_list is None:
            if isinstance(default, list):
                return default
            return []
        
        return [self._api_groups[i] for i in index_list]
    
    def find_name(self, model_name: str, default: list[ApiGroup] = None) -> List[ApiGroup]:
        """Find API groups by model name."""
        if self.CaseSensitive:
            key = model_name
        else:
            key = model_name.lower()

        index_list = self._api_names.get(key, None)
        if index_list is None:
            if isinstance(default, list):
                return default
            return []

        return [self._api_groups[i] for i in index_list]
    
    def find_baseGroup(self, group_name: str, default: list[ApiGroup] = None) -> List[ApiGroup]:
        """Find API groups by base group name."""
        if self.CaseSensitive:
            key = group_name
        else:
            key = group_name.lower()

        index_list = self._api_base_groups.get(key, None)
        if index_list is None:
            if isinstance(default, list):
                return default
            return []

        return [self._api_groups[i] for i in index_list]

    def find_task_type(self, task_type: str, default: list[ApiGroup] = None) -> List[ApiGroup]:
        """Find API groups by model task type."""
        if self.CaseSensitive:
            key = task_type
        else:
            key = task_type.lower()

        index_list = self._api_task_types.get(key, None)
        if index_list is None:
            if isinstance(default, list):
                return default
            return []

        return [self._api_groups[i] for i in index_list]
    
    def filter_with_expression(self, expression: str) -> list[ApiGroup]:
        """Filter API groups using a custom expression."""
        match = self._filter_expression_parser.match(expression)
        if not match:
            raise ValueError(f'Invalid filter expression: {expression}')
        
        find_mode = match.group('findmode')
        value = match.group('value')

        if find_mode == "uid":
            api_list = self.find_uid(value)
        elif find_mode == "name":
            api_list = self.find_name(value)
        elif find_mode == "base_group":
            api_list = self.find_baseGroup(value)
        elif find_mode == "task_type":
            api_list = self.find_task_type(value)
        else:
            raise ValueError(f'Unsupported find mode: {find_mode}')
        
        return api_list
