from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from typing import Iterable
import re

class CodeBlockExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(CodeBlockPreprocessor(md), "code_block", 30)

class CodeBlockPreprocessor(Preprocessor):
    FIND_BIG_CODE_BLOCK_PATTERN = re.compile(r"```(.*?)```", re.DOTALL)
    FIND_BIG_CODE_BLOCK_WITH_LANG_PATTERN = re.compile(r"```(.*?)(\n.*?)```", re.DOTALL)
    FIND_LITTLE_CODE_BLOCK_PATTERN = re.compile(r"`(.*?)`", re.DOTALL)

    def run(self, lines: Iterable[str]) -> Iterable[str]:
        # 合并文本
        text = "\n".join(lines)

        # 替换带语言的大代码块
        text = self.FIND_BIG_CODE_BLOCK_WITH_LANG_PATTERN.sub(r'<pre><code lang="\1">\2</code></pre>', text)

        # 替换大代码块
        text = self.FIND_BIG_CODE_BLOCK_PATTERN.sub(r"<pre><code>\1</code></pre>", text)

        # 替换小代码块
        text = self.FIND_LITTLE_CODE_BLOCK_PATTERN.sub(r"<code>\1</code>", text)

        # 将文本拆分成行
        lines = text.splitlines()

        return lines

def makeExtension(*args, **kwargs):
    return CodeBlockExtension(*args, **kwargs)