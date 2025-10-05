def remove_keys_from_dicts(dict_list: list[dict], keys_to_remove: list[str] | set[str]):
    """
    从字典列表中删除指定的键
    
    :param dict_list: 包含字典的列表
    :param keys_to_remove: 需要删除的键列表
    :return: 新的字典列表（原列表不被修改）
    """
    return [
        {k: v for k, v in d.items() if k not in keys_to_remove}
        for d in dict_list
    ]

def sum_string_lengths(items, field_name):
    """
    计算列表中所有字典指定字段的字符串长度总和
    
    :param items: 字典列表
    :param field_name: 要计算长度的字段名
    :return: 字符串长度总和
    """
    return sum(len(item[field_name]) for item in items if field_name in item and isinstance(item[field_name], str))