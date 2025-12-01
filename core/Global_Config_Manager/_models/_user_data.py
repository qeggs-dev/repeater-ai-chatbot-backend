from pydantic import BaseModel, ConfigDict

class Change_Data_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    context: bool = False
    prompt: bool = False
    config: bool = False


class User_Data_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    dir: str = "./workspace/data/user_data"
    branches_dir_name: str = "branches"
    metadata_file_name: str = "metadata.json"
    cache_medadata: bool | Change_Data_Config = False
    cache_data: bool | Change_Data_Config = False