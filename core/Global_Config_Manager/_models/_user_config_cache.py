from pydantic import BaseModel, ConfigDict

class User_Config_Cache_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    debounce_save_wait_time: float = 1000.0
    downgrade_wait_time: float = 600.0