# _styles.py
# Markdown 渲染样式预设 - 纯色主题

import os
import aiofiles
from pathlib import Path
from PathProcessors import validate_path, sanitize_filename
from loguru import logger

class Styles:
    def __init__(self, style_dir: str | os.PathLike):
        self._style_dir = Path(style_dir)
    
    @staticmethod
    async def _read_style(style_file_path: Path, encoding: str = "utf-8") -> str:
        if not style_file_path.exists():
            raise FileNotFoundError(f"Style file not found: {style_file_path}")
        if not style_file_path.is_file():
            raise ValueError(f"Style file must be a file: {style_file_path}")
        if not style_file_path.suffix == ".css":
            raise ValueError(f"Style file must be a .css file: {style_file_path}")
        
        async with aiofiles.open(style_file_path, 'r', encoding=encoding) as f:
            return await f.read()


    async def get_style(self, style_name: str, use_base: bool = True, encoding: str = "utf-8") -> str:
        style_name = sanitize_filename(style_name)
        style_file_path: Path = self._style_dir / f"{style_name}.css"

        if not validate_path(base_path = style_file_path, new_path = style_file_path):
            logger.warning(f"Style path validation failed: {style_file_path}")
            return BASE_STYLE
        
        try:
            return await self._read_style(style_file_path, encoding)
        except (FileNotFoundError, ValueError):
            if use_base:
                logger.warning(f"Style file not found: {style_file_path}")
                return BASE_STYLE
            else:
                logger.error(f"Style file not found: {style_file_path}")
                raise ValueError(f"Style file not found: {style_file_path}")
                

    def get_style_names(self) -> list[str]:
        basepath = self._style_dir
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