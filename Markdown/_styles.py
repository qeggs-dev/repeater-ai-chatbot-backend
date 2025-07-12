# md_styles.py
# Markdown 渲染样式预设 - 纯色主题

import aiofiles
from pathlib import Path
from ConfigManager import ConfigLoader
from PathProcessors import validate_path, sanitize_filename
from loguru import logger

configs = ConfigLoader()

async def _read_style(style_file_path: Path) -> str:
    if not style_file_path.exists():
        raise FileNotFoundError(f"Style file not found: {style_file_path}")
    if not style_file_path.is_file():
        raise ValueError(f"Style file must be a file: {style_file_path}")
    if not style_file_path.suffix == ".css":
        raise ValueError(f"Style file must be a .css file: {style_file_path}")
    
    async with aiofiles.open(style_file_path, 'r', encoding='utf-8') as f:
        return await f.read()


async def get_style(style_name: str, use_base: bool = True) -> str:
    style_name = sanitize_filename(style_name)
    basepath = configs.get_config("RENDER_STYLES_DIR", "./styles").get_value(Path)
    style_file_path = basepath / f"{style_name}.css"

    if not validate_path(base_path = basepath, new_path = style_file_path):
        raise ValueError(f"Invalid style file path: {style_file_path}")
    
    try:
        return await _read_style(style_file_path)
    except (FileNotFoundError, ValueError):
        if use_base:
            logger.warning(f"Style file not found: {style_file_path}", user_id = "[System]")
            return BASE_STYLE
        else:
            logger.error(f"Style file not found: {style_file_path}", user_id = "[System]")
            raise ValueError(f"Style file not found: {style_file_path}")
            

async def get_style_names() -> list[str]:
    basepath = configs.get_config("RENDER_STYLES_DIR", "./styles").get_value(Path)
    style_names = [f.stem for f in basepath.glob('*.css')]
    return style_names



BASE_STYLE = """
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  background-color: #ffffff;
  color: #333333;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  line-height: 1.7;
}

h1 {
  color: #2c3e50;
  margin-top: 1.2em;
  margin-bottom: 0.6em;
  font-weight: 600;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.3em;
  font-size: 2em;
}

h2 {
  color: #2c3e50;
  margin-top: 1.2em;
  margin-bottom: 0.6em;
  font-weight: 600;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.3em;
  font-size: 1.5em;
}

h3 {
  color: #2c3e50;
  margin-top: 1.2em;
  margin-bottom: 0.6em;
  font-weight: 600;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.3em;
  font-size: 1.17em;
}

h4 {
  color: #2c3e50;
  margin-top: 1.2em;
  margin-bottom: 0.6em;
  font-weight: 600;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.3em;
  font-size: 1em;
}

h5 {
  color: #2c3e50;
  margin-top: 1.2em;
  margin-bottom: 0.6em;
  font-weight: 600;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.3em;
  font-size: 0.83em;
}

h6 {
  color: #2c3e50;
  margin-top: 1.2em;
  margin-bottom: 0.6em;
  font-weight: 600;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.3em;
  font-size: 0.67em;
}

a {
  color: #3498db;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

code {
  background-color: #f8f9fa;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
}

pre {
  background-color: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
  overflow: auto;
  border-left: 4px solid #3498db;
}

blockquote {
  background-color: #f9f9f9;
  border-left: 4px solid #ddd;
  padding: 12px 20px;
  margin: 0;
  color: #555;
}

ul,
ol {
  padding-left: 28px;
}

li {
  margin-bottom: 8px;
}

img {
  max-width: 100%;
  border-radius: 6px;
  margin: 10px 0;
}

table {
  border-collapse: collapse;
  width: 100%;
  margin: 20px 0;
}

th,
td {
  border: 1px solid #e1e4e8;
  padding: 12px 15px;
  text-align: left;
}

th {
  background-color: #f6f8fa;
  font-weight: 600;
}

hr {
  border: 0;
  height: 1px;
  background: linear-gradient(
    to right,
    rgba(0, 0, 0, 0),
    rgba(0, 0, 0, 0.1),
    rgba(0, 0, 0, 0)
  );
  margin: 30px 0;
}
"""