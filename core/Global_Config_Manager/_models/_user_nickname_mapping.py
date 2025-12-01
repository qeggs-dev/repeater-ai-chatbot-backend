from pydantic import BaseModel, ConfigDict


class User_Nickname_Mapping_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    file_path: str = "./config/user_nickname_mapping.yml"