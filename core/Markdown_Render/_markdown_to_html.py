import html
import markdown
from ._extensions import (
    BrExtension,
    CodeBlockExtension,
    DividingLineExtension
)
from TextProcessors import PromptVP

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
    
    # 2. 转义以安全包含内容
    markdown_text = html.escape(markdown_text)
    
    # 3. 渲染 Markdown 为 HTML
    html_content = markdown.markdown(
        markdown_text,
        extensions=[
            CodeBlockExtension(),
            BrExtension(),
            DividingLineExtension(),
        ]
    )

    # 4. 预处理 HTML 文本
    if preprocess_map_after:
        for key, value in preprocess_map_after.items():
            html_content = html_content.replace(key, value)
    
    # 5. 添加自适应宽度
    css += f"\nbody {{ width: {max(width, 60) - 60}px; }}"

    template_handler = PromptVP()
    template_handler.bulk_register_variable(
        html_content = html_content,
        css = css,
        title = html.escape(title)
    )

    # 6. 生成 HTML 文本
    full_html = template_handler.process(html_template)
    return full_html