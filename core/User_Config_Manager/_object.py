from pydantic import BaseModel, ConfigDict, Field

class UserConfigs(BaseModel):
    """
    Configs for user.
    """
    model_config = ConfigDict(validate_assignment=True)

    timezone: int | None = Field(None, ge=-12, le=12)
    parset_prompt_name: str | None = None
    model_uid: str | None = None
    temperature: float | None = Field(None, ge=0.0, le=2.0)
    top_p: float | None = Field(None, ge=0.0, le=1.0)
    max_tokens: int | None = None
    max_completion_tokens: int | None = None
    stop: list[str] | None = None
    frequency_penalty: float | None = Field(None, ge=-2.0, le=2.0)
    presence_penalty: float | None = Field(None, ge=-2.0, le=2.0)
    auto_shrink_length: int | None = None
    render_style: str | None = None
    render_html_template: str | None = None
    load_prompt: bool = True
    save_context: bool = True