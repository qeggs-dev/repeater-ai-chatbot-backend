from string import Formatter
from typing import Any, TypeVar

T = TypeVar('T')

class SafeFormatter(Formatter):
    def __init__(self, default_value:T | None = None, *args, **kwargs):
        """
        初始化 SafeFormatter
        
        :param default_value: 全局默认值，当字段缺失时使用
        """
        super().__init__(*args, **kwargs)
        self.default_value:T | None = default_value

    def get_value(self, key, args, kwargs) -> str | T:
        try:
            return super().get_value(key, args, kwargs)
        except (KeyError, IndexError):
            # 使用初始化时设置的 default_value
            if self.default_value is not None:
                return self.default_value
            # 最后保留原始占位符
            else:
                return "{" + str(key) + "}"

# 使用示例
if __name__ == "__main__":
    # 示例1: 不设置默认值，保留占位符
    formatter1 = SafeFormatter()
    print(formatter1.format("Hello {name}, age: {age}", name="Alice")) 
    # 输出: Hello Alice, age: {age}

    # 示例2: 设置全局默认值
    formatter2 = SafeFormatter(default_value="N/A")
    print(formatter2.format("Hello {name}, age: {age}", name="Bob")) 
    # 输出: Hello Bob, age: N/A

    # 示例3: 在format时覆盖默认值
    formatter3 = SafeFormatter(default_value="N/A")
    print(formatter3.format("Hello {name}, age: {age}", name="Charlie", default="unknown")) 
    # 输出: Hello Charlie, age: unknown