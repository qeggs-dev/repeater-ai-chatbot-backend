from typing import Callable

def create_chars_remover(old_chars: str, new_char: str):
    if len(new_char) != 1:
        raise ValueError('new_char must be a single character')
    trans_table = str.maketrans(old_chars, new_char * len(old_chars))
    def remover(text: str):
        # 先处理ASCII字符
        result = text.translate(trans_table)
        return result
    return remover


def create_special_chars_remover(new_char: str):
    delete_chars = []
    for i in range(32, 127):
        c = chr(i)
        if not (('A' <= c <= 'Z') or ('a' <= c <= 'z') or ('0' <= c <= '9') or c == '_'):
            delete_chars.append(c)

    delete_str = ''.join(delete_chars)
    return create_chars_remover(delete_str, new_char)