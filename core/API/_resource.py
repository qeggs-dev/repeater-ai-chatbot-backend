# ==== 第三方库 ==== #
from environs import Env
env = Env()
from fastapi import FastAPI

# ==== 自定义库 ==== #
from .._core import Core
from AdminApikeyManager import AdminKeyManager
from ._lifespan import lifespan
from ..Global_Config_Manager import ConfigManager
from ..Markdown_Render import HTML_Render
# endregion

# region Global Objects
app = FastAPI(
    title="RepeaterChatBackend",
    lifespan = lifespan
)
chat = Core()

# 生成或读取API Key
admin_api_key = AdminKeyManager()

render_config = ConfigManager.get_configs().render
browser_pool_manager = HTML_Render.BrowserPoolManager(
    max_pages_per_browser = render_config.to_image.max_pages_per_browser,
    max_browsers = render_config.to_image.max_browsers,
    default_browser = render_config.to_image.browser_type,
    headless = render_config.to_image.headless,
    browser_args = HTML_Render.BrowserArgs(
        render_config.to_image.executable_path
    )
)

__version__ = "2.0.1.0"