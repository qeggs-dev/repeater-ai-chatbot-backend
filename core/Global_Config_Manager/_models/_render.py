from pydantic import BaseModel, ConfigDict, Field
from ...Markdown_Render import HTML_Render

class Preprocess_Map_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    before: dict[str, str] = Field(default_factory=dict)
    after: dict[str, str] = Field(default_factory=dict)

class Render_Markdown_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    default_style: str = "light"
    styles_dir: str = "./configs/styles"
    style_file_encoding: str = "utf-8"
    html_template_dir: str = "./configs/html_templates"
    html_template_file_encoding: str = "utf-8"
    default_html_template: str = "default.html"
    preprocess_map: Preprocess_Map_Config = Field(default_factory=Preprocess_Map_Config)
    title: str = "Repeater Image Generator"

class Markdwn_To_Image_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    output_dir: str = "./workspace/temp/render"
    max_pages_per_browser: int = 5,
    max_browsers: int = 2,
    browser_type: HTML_Render.BrowserType = HTML_Render.BrowserType.AUTO,
    headless: bool = True
    output_suffix: str = ".png"
    executable_path: str = None
    width: int = 1200
    height: int = 600
    quality: int = 90

class Render_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    default_image_timeout: float = 60.0

    markdown: Render_Markdown_Config = Field(default_factory=Render_Markdown_Config)
    to_image: Markdwn_To_Image_Config = Field(default_factory=Markdwn_To_Image_Config)