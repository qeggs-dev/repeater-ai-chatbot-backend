from pydantic import BaseModel, Field, ConfigDict
from ._preprocess_map import Preprocess_Map_Config

class Markdown_To_HTML_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    default_style: str = "light"
    styles_dir: str = "./configs/styles"
    style_file_encoding: str = "utf-8"
    html_template_dir: str = "./configs/html_templates"
    html_template_file_encoding: str = "utf-8"
    default_html_template: str = "default"
    html_template_suffix: str = ".html"
    preprocess_map: Preprocess_Map_Config = Field(default_factory=Preprocess_Map_Config)
    title: str = "Repeater Image Generator"