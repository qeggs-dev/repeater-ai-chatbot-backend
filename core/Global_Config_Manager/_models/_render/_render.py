from pydantic import BaseModel, ConfigDict, Field
from ._markdown_to_html import Markdown_To_HTML_Config
from ._html_to_image import HTML_To_Image_Config

class Render_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    default_image_timeout: float = 60.0

    markdown: Markdown_To_HTML_Config = Field(default_factory=Markdown_To_HTML_Config)
    to_image: HTML_To_Image_Config = Field(default_factory=HTML_To_Image_Config)