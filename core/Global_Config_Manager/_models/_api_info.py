from pydantic import BaseModel, ConfigDict

class API_Info_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)
    
    api_file_path: str = "./config/apiconfig.json"
    default_model_uid: str = "deepseek-chat"