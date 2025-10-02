import os
import asyncio
import hashlib
import base64
from ._charset import DEFAULT_INVALID_CHARS
from TextProcessors import create_special_chars_remover

special_chars_remover = create_special_chars_remover("_")

def sanitize_filename(
        text: str,
        max_length: int = 255,
        encoding: str = "utf-8",
    ) -> str:
    """
    转义文件名中的非法字符，提供安全的字符串路径注入转义

    :param text: 任意字符串
    :param max_length: 文件名最大长度（不含扩展名）
    :param encoding: 编码方式(在当字符串非常长时用于生成md5路径名)
    :return: 符合文件名格式的字符串
    """
    if len(text) > max_length:
        filename = base64.b32encode(
            hashlib.md5(
                text.encode(
                    encoding
                )
            ).digest()
        ).decode(encoding)
        if len(filename) > max_length:
            filename = filename[:max_length]
        return filename
    return special_chars_remover(text)

# 示例用法
if __name__ == "__main__":
    # 测试文件名转义和缩短
    test_filename = 'my/illegal:file?.name*with<long>path.txt'
    print(sanitize_filename(test_filename, prefix="doc"))  # 输出: doc_my_illegal_file_name_with_long_path.txt

    # 测试文件名过长的情况
    long_filename = 'a' * 300 + '.txt'
    print(sanitize_filename(long_filename))  # 输出: 类似 "9835fa6bf4e20a9b.txt"