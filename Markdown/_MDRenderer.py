import markdown
import imgkit
import asyncio
from pathlib import Path
from ._styles import get_style, get_style_names
from ConfigManager import ConfigLoader

configs = ConfigLoader()

# 修改 markdown_to_image 函数
async def markdown_to_image(
    markdown_text: str,
    output_path: str,
    width: int = 800,
    css: str | None = None,
    style: str = "light",
    preprocess_map_before: dict[str, str] | None = None,
    preprocess_map_end: dict[str, str] | None = None,
    options: dict = None
) -> str:
    """
    使用 wkhtmltoimage 将 Markdown 转为自适应图片
    
    参数:
    - markdown_text: Markdown 文本
    - output_path: 输出图片路径 (.png/.jpg)
    - width: 目标宽度 (像素)
    - css: 自定义 CSS 样式 (优先级高于style参数)
    - style: 预设样式名称 (light/dark/pink/blue/green)
    - preprocess_map_before: 渲染前自定义字符映射
    - preprocess_map_end: 渲染后自定义字符映射
    - options: wkhtmltoimage 高级选项
    
    返回: 输出文件路径
    """
    if preprocess_map_before:
        for key, value in preprocess_map_before.items():
            markdown_text = markdown_text.replace(key, value)
    
    # 1. 渲染 Markdown 为 HTML
    html_content = markdown.markdown(markdown_text)
    
    # 2. 构建完整 HTML
    if css is None:
        # 使用预设样式
        css = await get_style(style)
    
    # 添加自适应宽度
    css += f"\nbody {{ width: {width - 60}px; }}"
    
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>{css}</style>
    </head>
    <body>{html_content}</body>
    </html>
    """

    if preprocess_map_end:
        for key, value in preprocess_map_end.items():
            full_html = full_html.replace(key, value)
    
    # 3. 配置转换选项
    default_options = {
        'enable-local-file-access': None, # 允许本地文件
        'encoding': "UTF-8",              # 编码设置
        'quiet': ''                       # 静默模式
    }
    if options:
        default_options.update(options)
    
    # 4. 转换并保存图片
    wkhtmltoimage_path = configs.get_config("wkhtmltoimage_path").get_value(Path)
    config = imgkit.config(wkhtmltoimage=wkhtmltoimage_path)
    await asyncio.to_thread(
        imgkit.from_string,
        string = full_html,
        output_path = output_path,
        config = config,
        options = default_options
    )
    
    return str(Path(output_path).resolve())