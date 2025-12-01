# ==== 第三方库 ==== #
from environs import Env
env = Env()
from fastapi import FastAPI

# ==== 自定义库 ==== #
from ..Global_Config_Manager import ConfigLoader
from .._core import Core
from AdminApikeyManager import AdminKeyManager
from PathProcessors import validate_path
# endregion

# region Global Objects
app = FastAPI(title="RepeaterChatBackend")
chat = Core()

# 生成或读取API Key
admin_api_key = AdminKeyManager()