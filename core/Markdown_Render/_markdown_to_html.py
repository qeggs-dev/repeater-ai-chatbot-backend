import os
import markdown
from pathlib import Path
from ._br_extension import BrExtension
from ._styles import Styles
from TextProcessors import PromptVP

# 修改 markdown_to_image 函数
async def markdown_to_html(
    markdown_text: str,
    html_template: str,
    css: str,
    title: str = "Markdown Render",
    width: int = 800,
    preprocess_map_before: dict[str, str] | None = None,
    preprocess_map_after: dict[str, str] | None = None,
) -> str:
    """
    使用 wkhtmltoimage 将 Markdown 转为 HTML
    
    参数:
    - markdown_text: Markdown 文本
    - width: 目标宽度 (像素)
    - css: 自定义 CSS 样式 (优先级高于style参数)
    - style: 预设样式名称 (light/dark/pink/blue/green)
    - preprocess_map_before: 渲染前自定义字符映射
    - preprocess_map_end: 渲染后自定义字符映射
    
    返回: 输出文件路径
    """
    # 1. 预处理 Markdown 文本
    if preprocess_map_before:
        for key, value in preprocess_map_before.items():
            markdown_text = markdown_text.replace(key, value)
    
    # 2. 渲染 Markdown 为 HTML
    html_content = markdown.markdown(markdown_text, extensions=[BrExtension()])

    # 3. 预处理 HTML 文本
    if preprocess_map_after:
        for key, value in preprocess_map_after.items():
            html_content = html_content.replace(key, value)
    
    # 4. 添加自适应宽度
    css += f"\nbody {{ width: {max(width, 60) - 60}px; }}"
    
    template_handler = PromptVP()
    template_handler.register_variable(
        name = "html_content",
        value = html_content
    )
    template_handler.register_variable(
        name = "css",
        value = css
    )
    template_handler.register_variable(
        name = "title",
        value = title
    )

    # 5. 生成 HTML 文本
    full_html = template_handler.process(html_template)
    return full_html