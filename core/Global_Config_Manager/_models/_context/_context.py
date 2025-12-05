from pydantic import BaseModel, ConfigDict

class Context_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    auto_shrink_length: int | None = None