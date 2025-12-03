# ==== 第三方库 ==== #
from environs import Env
env = Env()
from fastapi import FastAPI

# ==== 自定义库 ==== #
from .._core import Core
from AdminApikeyManager import AdminKeyManager
from PathProcessors import validate_path
from ._lifespan import lifespan
# endregion

# region Global Objects
app = FastAPI(
    title="RepeaterChatBackend",
    lifespan = lifespan
)
chat = Core()

# 生成或读取API Key
admin_api_key = AdminKeyManager()

__version__ = "2.0.0.1"