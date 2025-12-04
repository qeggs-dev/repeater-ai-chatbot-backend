import markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
import re

class BrExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(BrPreprocessor(md), 'br_extension', 15)

class BrPreprocessor(Preprocessor):
    FIND_PATTERN = re.compile(r'```.*?```', re.DOTALL)
    SUB_PATTERN = re.compile(r'\n+')
    def run(self, lines):
        text = '\n'.join(lines)
        
        # 使用正则表达式匹配代码块
        parts = []
        last_end = 0
        
        # 查找所有代码块
        for match in self.FIND_PATTERN.finditer(text):
            # 添加代码块之前的内容（处理换行符）
            before_code = text[last_end:match.start()]
            before_code_processed = self.SUB_PATTERN.sub('<br>\n', before_code)
            parts.append(before_code_processed)
            
            # 添加代码块（保持原样）
            parts.append(match.group())
            last_end = match.end()
        
        # 添加剩余内容
        if last_end < len(text):
            remaining = text[last_end:]
            remaining_processed = self.SUB_PATTERN.sub('<br>\n', remaining)
            parts.append(remaining_processed)
        
        # 重新分割为行
        result_text = ''.join(parts)
        return result_text.split('\n')

def makeExtension(**kwargs):
    return BrExtension(**kwargs)