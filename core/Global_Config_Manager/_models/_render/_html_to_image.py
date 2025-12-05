from pydantic import BaseModel, ConfigDict
from ....Markdown_Render import HTML_Render

class HTML_To_Image_Config(BaseModel):
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