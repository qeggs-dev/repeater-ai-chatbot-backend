from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Sequence
from playwright.async_api import ProxySettings

@dataclass
class BrowserArgs:
    executable_path: Path | str | None = None
    channel: str | None = None
    args: Sequence[str] | None = None
    ignore_default_args: bool | Sequence[str] | None = None
    handle_sigint: bool | None = None
    handle_sigterm: bool | None = None
    handle_sighup: bool | None = None
    timeout: float | None = None
    env: dict[str, str | float | bool] | None = None
    headless: bool | None = None
    devtools: bool | None = None
    proxy: ProxySettings | None = None
    downloads_path: Path | str | None = None
    slow_mo: float | None = None
    traces_dir: Path | str | None = None
    chromium_sandbox: bool | None = None
    firefox_user_prefs: dict[str, str | float | bool] | None = None

    @property
    def as_dict(self) -> dict[str, Any]:
        return asdict(self)