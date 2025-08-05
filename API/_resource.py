# region imports
# ==== 标准库 ==== #
from pathlib import Path

# ==== 第三方库 ==== #
from environs import Env
env = Env()
from fastapi import FastAPI

# ==== 自定义库 ==== #
from ConfigManager import ConfigLoader
# 一定要提前加载，否则其他模块会无法获取配置内容
configs = ConfigLoader(
    config_file_path = env.path("CONFIG_FILE_PATH", "./configs/project_config.json")
)
import core
from AdminApikeyManager import AdminKeyManager
from PathProcessors import validate_path
# endregion

# region Global Objects
app = FastAPI(title="RepeaterChatBackend")
chat = core.Core()

# 生成或读取API Key
admin_api_key = AdminKeyManager()
# endregion

# region Tool: validate_path
def validate_path(base_path: str | Path, user_path: str | Path) -> bool:
    """
    验证路径是否合法
    """
    # 转换为Path对象以便于操作
    base_path = Path(base_path)
    user_path = Path(user_path)

    # 获取基础路径的绝对路径
    requested_path = (base_path.resolve() / user_path).resolve()
    
    # 检查路径是否在base_path的子目录内
    return requested_path.is_relative_to(base_path.resolve())
# endregion