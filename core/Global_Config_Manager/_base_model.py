from pydantic import BaseModel, ConfigDict, Field
from ._models import *

class Base_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    api_info: API_Info_Config = Field(default_factory=API_Info_Config)
    blacklist: Backlist_Config = Field(default_factory=Backlist_Config)
    bot_info: Bot_Info_Config = Field(default_factory=Bot_Info_Config)
    callapi: CallAPI_Config = Field(default_factory=CallAPI_Config)
    context: Context_Config = Field(default_factory=Context_Config)
    core: Core_Config = Field(default_factory=Core_Config)
    logger: Logger_Config = Field(default_factory=Logger_Config)
    model: Model_Config = Field(default_factory=Model_Config)
    prompt: Prompt_Config = Field(default_factory=Prompt_Config)
    render: Render_Config = Field(default_factory=Render_Config)
    request_log: Request_Log_Config = Field(default_factory=Request_Log_Config)
    server: Server_Config = Field(default_factory=Server_Config)
    static: Static_Config = Field(default_factory=Static_Config)
    time: Time_Config = Field(default_factory=Time_Config)
    user_config_cache: User_Config_Cache_Config = Field(default_factory=User_Config_Cache_Config)
    user_data: User_Data_Config = Field(default_factory=User_Data_Config)
    user_nickname_mapping: User_Nickname_Mapping_Config = Field(default_factory=User_Nickname_Mapping_Config)
    web: Web_Config = Field(default_factory=Web_Config)