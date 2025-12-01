from pydantic import BaseModel, ConfigDict

class Prompt_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    dir: str = "./config/prompt/presets"
    suffix: str = ".md"
    encoding: str = "utf-8"
    preset_name: str = "default"