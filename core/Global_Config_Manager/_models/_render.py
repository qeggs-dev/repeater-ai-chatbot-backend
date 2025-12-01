from pydantic import BaseModel, ConfigDict, Field

class Preprocess_Map_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    before: dict[str, str] = Field(default_factory=dict)
    after: dict[str, str] = Field(default_factory=dict)
    

class Markdwn_To_Image_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    default_style: str = "light"
    styles_dir: str = "./config/styles"
    style_file_encoding: str = "utf-8"
    preprocess_map: Preprocess_Map_Config = Field(default_factory=Preprocess_Map_Config)
    wkhtmltoimage_path: str = "wkhtmltoimage"
    output_dir: str = "./workspace/temp/render"


class Render_Markdown_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    to_image: Markdwn_To_Image_Config = Field(default_factory=Markdwn_To_Image_Config)
    

class Render_Config(BaseModel):
    model_config = ConfigDict(case_sensitive=False)

    default_image_timeout: float = 60.0
    markdown: Render_Markdown_Config = Field(default_factory=Render_Markdown_Config)