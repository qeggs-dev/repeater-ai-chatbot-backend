from pydantic import BaseModel, ConfigDict
from ..CallAPI import CompletionsAPI

class Response(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
    )

    reasoning_content: str = ""
    content: str = ""
    user_raw_input: str = ""
    user_input: str = ""
    model_group: str = ""
    model_name: str = ""
    model_type: str = ""
    model_uid: str = ""
    create_time: int = 0
    id: str = ""
    finish_reason_cause: str = ""
    finish_reason_code: CompletionsAPI.FinishReason | None = None
    status: int = 200