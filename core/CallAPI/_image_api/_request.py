from dataclasses import dataclass
from typing import Literal
from enum import StrEnum

class ImageSize(StrEnum):
    AUTO = "auto"
    Square_1024 = "1024x1024"
    Three_by_Two_512x = "1536x1024"
    Two_by_Three_3x = "1024x1536"
    Square_256 = "256x256"
    Square_512 = "512x512"
    Seven_by_Four_256x = "1792x1024"
    Four_by_Seven_7x = "1024x1792"

@dataclass
class Request:
    """
    This class is used to store the request data for the image API.
    """
    base_url: str = ""
    api_key: str = ""
    model: str = ""
    size: ImageSize | str = ImageSize.Square_1024
    prompt: str = ""
    n: int = 1