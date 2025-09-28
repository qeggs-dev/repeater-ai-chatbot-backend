from dataclasses import dataclass
from bs4 import BeautifulSoup, Tag
from typing import List

@dataclass
class LabelReplaceObj:
    """
    This object will tell the replacer exactly how you need to replace the label.

    ---

    :param replace: The text to replace.
    :param parent: The parent element to replace.
    :param inverted: If enabled, the parent of the item must not exist.
    """
    replace: str
    parent: List[str] | None = None
    inverted: bool = False


class HTMLTagReplacer:
    def __init__(self):
        self.soup = None
    
    def replace_tags(self, html_content: str, replace_objs: List[LabelReplaceObj]) -> str:
        """
        根据提供的替换对象列表替换HTML中的标签
        
        :param html_content: 原始HTML内容
        :param replace_objs: 替换规则列表
        :return: 处理后的HTML内容
        """
        # 解析HTML
        self.soup = BeautifulSoup(html_content, 'html.parser')
        
        # 对每个替换规则进行处理
        for replace_obj in replace_objs:
            self._process_replace_obj(replace_obj)
        
        return str(self.soup)
    
    def _process_replace_obj(self, replace_obj: LabelReplaceObj):
        """处理单个替换规则"""
        # 查找所有需要替换的文本
        text_nodes = self.soup.find_all(string=lambda text: replace_obj.replace in text)
        
        for text_node in text_nodes:
            # 检查父级条件
            if self._check_parent_condition(text_node, replace_obj.parent, replace_obj.inverted):
                # 替换文本
                new_text = text_node.replace(replace_obj.replace, f"<replaced>{replace_obj.replace}</replaced>")
                new_soup = BeautifulSoup(new_text, 'html.parser')
                
                # 用新内容替换旧文本节点
                text_node.replace_with(new_soup)
    
    def _check_parent_condition(self, element, parent_tags: List[str] | None, inverted: bool) -> bool:
        """
        检查元素的父级条件是否满足
        
        :param element: 要检查的元素
        :param parent_tags: 要求的父级标签列表
        :param inverted: 是否反转条件
        :return: 是否满足条件
        """
        if parent_tags is None:
            return True
        
        # 获取所有父级标签
        current = element.parent
        parent_found = False
        
        while current and current.name != '[document]':
            if current.name in parent_tags:
                parent_found = True
                break
            current = current.parent
        
        # 根据inverted标志返回结果
        return parent_found if not inverted else not parent_found


# 使用示例
def example_usage():
    # 示例HTML内容
    html_content = """
    <html>
        <body>
            <div class="content">
                <p>这是一个需要替换的文本</p>
                <div class="special">
                    <span>这也是一个需要替换的文本</span>
                </div>
                <section>
                    <article>
                        <p>这又是一个需要替换的文本</p>
                    </article>
                </section>
            </div>
        </body>
    </html>
    """
    
    # 定义替换规则
    replace_objs = [
        # 替换所有"需要替换的文本"，不限制父级
        LabelReplaceObj(
            replace="需要替换的文本",
            parent=None,
            inverted=False
        ),
        # 只在父级有div标签时替换"需要替换的文本"
        LabelReplaceObj(
            replace="需要替换的文本",
            parent=["div"],
            inverted=False
        ),
        # 只在父级没有section标签时替换"需要替换的文本"
        LabelReplaceObj(
            replace="需要替换的文本",
            parent=["section"],
            inverted=True
        ),
    ]
    
    # 创建替换器并执行替换
    replacer = HTMLTagReplacer()
    result = replacer.replace_tags(html_content, replace_objs)
    
    print("原始HTML:")
    print(html_content)
    print("\n处理后的HTML:")
    print(result)


if __name__ == "__main__":
    example_usage()