from environs import Env as _Env
from . import Global_Config_Manager
_env = _Env()
config_loader = Global_Config_Manager.ConfigManager()
config_loader.update_base_path(
    _env.path("CONFIG_DIR", "./configs/project_configs"),
    _env.json("CONFIG_FORCE_LOAD_LIST", None)
)
config_loader.load(
    create_if_missing=True
)
from . import API
__api_version__ = API.__version__
from . import Logger_Init
from ._core import Core, Response
from ._info import (
    __version__,
    __author__,
    __license__,
    __copyright__,
)
from . import Request_User_Info
from . import User_Config_Manager
from . import ApiInfo
from . import Data_Manager
from . import CallAPI
from . import Request_Log
from . import Context_Manager