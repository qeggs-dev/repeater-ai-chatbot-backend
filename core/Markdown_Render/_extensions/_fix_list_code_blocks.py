from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from xml.etree.ElementTree import Element

class FixListCodeExtension(Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(FixListCodeBlocks(md), "fixlistcode", 15)

class FixListCodeBlocks(Treeprocessor):
    def run(self, root: Element) -> Element:
        # 查找所有包含代码块的li元素
        for li in root.findall(".//li"):
            pre_elements: list[Element[str]] = li.findall("pre")
            if pre_elements:
                # 将pre元素从li中移出，放到li后面
                parent = li.getparent()
                idx = list(parent).index(li)
                for pre in pre_elements:
                    li.remove(pre)
                    parent.insert(idx + 1, pre)
        return root