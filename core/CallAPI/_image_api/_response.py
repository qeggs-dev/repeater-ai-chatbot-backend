from dataclasses import dataclass, field


@dataclass
class Response:
    """
    This class is used to store the response data for the image API.
    """
    created: int = 0
    images: list[str] = field(default_factory=list)