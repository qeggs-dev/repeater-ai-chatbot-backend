from dataclasses import dataclass, asdict

@dataclass
class Response:
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
    status: int = 200

    @property
    def as_dict(self):
        return asdict(self)