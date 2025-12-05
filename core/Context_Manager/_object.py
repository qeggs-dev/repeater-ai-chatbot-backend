from __future__ import annotations
from dataclasses import dataclass, field
from typing import overload, Iterable
from enum import Enum
from ._exceptions import *
from ._func_calling_obj import CallingFunctionResponse

class ContextRole(Enum):
    """
    上下文角色
    """
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "tool"

@dataclass
class ContentUnit:
    """
    上下文单元
    """
    reasoning_content:str = ""
    content: str = ""
    role: ContextRole = ContextRole.USER
    role_name: str |  None = None
    prefix: bool | None = None
    funcResponse: CallingFunctionResponse | None = None
    tool_call_id: str = ""

    def __len__(self):
        length = 0
        if self.reasoning_content:
            length += len(self.reasoning_content)
        else:
            length += len(self.content)
        return length
    
    def update_from_content(self, content: dict) -> None:
        """
        更新上下文内容
        :param content: 上下文内容
        :return: None
        """
        other = self.from_content(content)
        self.reasoning_content = other.reasoning_content
        self.content = other.content
        self.role = other.role
        self.role_name = other.role_name
        self.prefix = other.prefix
        self.funcResponse = other.funcResponse
        self.tool_call_id = other.tool_call_id
    
    # 导出为列表
    def to_content(self, remove_resoning_prompt: bool = False) -> list[dict]:
        """
        OpenAI Message兼容格式列表单元

        :param remove_reasoner_prompt: 是否移除reasoner提示
        :return: OpenAI Message兼容格式列表单元
        """
        content_list = []
        if self.content:
            if self.role in {ContextRole.SYSTEM, ContextRole.USER}:
                content = {
                    "role": self.role.value,
                    "content": self.content
                }
                if self.role_name:
                    content["name"] = self.role_name
                content_list.append(content)

            elif self.role == ContextRole.ASSISTANT:
                assistant_content = {
                    "role": self.role.value,
                    "content": self.content,
                }
                if self.role_name:
                    assistant_content["name"] = self.role_name
                if self.prefix:
                    assistant_content["prefix"] = self.prefix
                if not remove_resoning_prompt and self.reasoning_content:
                    assistant_content["reasoning_content"] = self.reasoning_content
                if self.funcResponse:
                    assistant_content["tool_calls"] = self.funcResponse.as_calling_func_content
                content_list.append(assistant_content)
        if self.funcResponse:
            if self.role == ContextRole.FUNCTION:
                tool_content = {
                    "role": self.role.value,
                    "content": self.content,
                    "tool_call_id": self.tool_call_id
                }
                content_list.append(tool_content)
        
        return content_list
    
    @property
    def as_content(self):
        """
        获取Context的OpenAI Message兼容格式列表单元

        :return: OpenAI Message兼容格式列表单元
        """
        self.to_content(False)
    
    # 从列表中加载内容
    @classmethod
    def from_content(cls, context: dict):
        """
        从Message列表单元中加载内容

        :param context: OpenAI Message兼容格式列表单元
        :return: Context
        """
        content = cls()

        if "role" not in context:
            raise ContextNecessaryFieldsMissingError("Not found role field")
        elif not isinstance(context["role"], str):
            raise ContextFieldTypeError("role field is not str")
        elif context["role"] not in [role.value for role in ContextRole]:
            raise ContextInvalidRoleError(f"Invalid role: {context['role']}")
        else:
            try:
                content.role = ContextRole(context["role"])
            except ValueError:
                raise ContextInvalidRoleError(f"Invalid role: {context['role']}")
        
        if "content" not in context:
            raise ContextNecessaryFieldsMissingError("Not found content field")
        elif not isinstance(context["content"], str):
            raise ContextFieldTypeError("content field is not str")
        else:
            content.content = context["content"]
        
        if "reasoning_content" in context:
            if not isinstance(context["reasoning_content"], str):
                raise ContextFieldTypeError("reasoning_content field is not str")
            else:
                content.reasoning_content = context["reasoning_content"]
        
        if "prefix" in context:
            if not isinstance(context["prefix"], bool):
                raise ContextFieldTypeError("prefix field is not bool")
            else:
                content.prefix = context["prefix"]
        
        if content.role == ContextRole.ASSISTANT:
            if "tool_calls" in context:
                if not content.funcResponse:
                    content.funcResponse = CallingFunctionResponse()
                content.funcResponse.update_from_dict(context["tool_calls"])
        
        if content.role == ContextRole.FUNCTION:
            if "tool_call_id" not in context:
                raise ContextNecessaryFieldsMissingError("Not found tool_call_id field")
            elif not isinstance(context['tool_call_id'], str):
                raise ContextFieldTypeError("tool_call_id field is not str")
            else:
                content.tool_call_id = context["tool_call_id"]
        
        return content

@dataclass
class ContextObject:
    """
    上下文对象
    """
    prompt: ContentUnit | None = None
    context_list: list[ContentUnit] = field(default_factory=list)

    @overload
    def __getitem__(self, index: int) -> ContentUnit:
        ...

    @overload
    def __getitem__(self, index: slice) -> ContextObject:
        ...
    
    def __getitem__(self, index: int | slice):
        """
        获取上下文列表中的指定项
        
        :param index: 索引
        :return: 指定项
        """
        if isinstance(index, int):
            return self.context_list[index]
        elif isinstance(index, slice):
            return ContextObject(prompt=self.prompt, context_list=self.context_list[index])
        else:
            raise TypeError("index must be int or slice")
    
    def __setitem__(self, index: int | slice, value: ContentUnit | Iterable[ContentUnit]):
        """
        设置上下文列表中的指定项
        
        :param index: 索引
        :param value: 值
        :return: 构建的对象
        """
        self.context_list[index] = value

    def __len__(self):
        """
        获取上下文列表的长度

        :return: 上下文列表的长度
        """
        return self.context_item_length
    
    def __iter__(self):
        """
        迭代上下文列表
        
        :return: 上下文列表的迭代器
        """
        # 先 yield 提示词
        if self.prompt:
            yield self.prompt
        # 再正常遍历 context_list
        for content in self.context_list:
            yield content

    
    def update_from_context(self, context: list[dict]) -> None:
        """
        从上下文列表更新上下文
        
        :param context: 上下文列表
        :return: 构建的对象
        """
        other = self.from_context(context)
        self.context_list = other.context_list
        self.prompt = other.prompt
    
    @property
    def context_item_length(self):
        """
        获取上下文列表的长度
        
        :return: 上下文列表的长度
        """
        return len(self.context_list)

    @property
    def total_length(self) -> int:
        """
        获取上下文总长度
        
        :return: 上下文总长度
        """
        return (
            sum(
                [len(content) for content in self.context_list]
            )
            +
            (
                len(self.prompt) if self.prompt else 0
            )
        )
    
    @property
    def average_length(self) -> float:
        """
        获取上下文平均长度

        :return: 上下文平均长度
        """
        return self.total_length / len(self.context_list)

    def to_context(self, remove_resoning_prompt: bool = False) -> list[dict]:
        """
        获取上下文

        :param remove_reasoner_prompt: 是否移除reasoner提示词
        """
        context_list = []
        if self.context_list:
            for content in self.context_list:
                context_list += content.to_content(remove_resoning_prompt)
        return context_list
    
    @property
    def context(self) -> list[dict]:
        """
        获取上下文
        """
        return self.to_context(False)
    
    def to_full_context(self, remove_resoning_prompt: bool = False) -> list[dict]:
        """
        获取上下文，如果有提示词，则添加到最前面

        :param remove_reasoner_prompt: 是否移除reasoner提示词
        """
        context_list = self.to_context(remove_resoning_prompt)
        if self.prompt:
            context_list = self.prompt.to_content(remove_resoning_prompt) + context_list
        return context_list
    
    @property
    def full_context(self) -> list[dict]:
        """
        获取上下文，如果有提示词，则添加到最前面
        """
        return self.to_full_context(False)
    
    def withdraw(self, length: int | None = None):
        """
        撤销指定长度的内容

        :param length: 撤销长度
        :return: 撤销的内容
        """
        if length is None:
            pop_items: list[ContentUnit] = []
            
            # 安全检查
            if not self.context_list:
                return ContextObject()
            try:
                # 第一步：pop直到找到助手消息
                while (self.context_list and 
                    self.last_content.role != ContextRole.ASSISTANT):
                    pop_items.append(self.context_list.pop())
                
                # 第二步：pop助手消息
                while (self.context_list and 
                    self.last_content.role == ContextRole.ASSISTANT):
                    pop_items.append(self.context_list.pop())
                
                # 第三步：pop相关联的用户消息
                while (self.context_list and 
                    self.last_content.role != ContextRole.ASSISTANT):
                    pop_items.append(self.context_list.pop())
            except IndexError:
                pass
            
            return ContextObject(
                prompt = None,
                context_list = pop_items[::-1],
            )
        elif isinstance(length, int):
            if length > len(self.context_list):
                raise ValueError("length is too long")
            if length <= 0:
                raise ValueError("length is too short")
            
            # 检查索引是否在上下文范围内
            if 0 <= length < len(self.context_list):
                return self.pop_last_n(length)
            else:
                raise IndexError("Index out of range")
        else:
            raise TypeError("length must be int or None")
    
    def insert(self, content_unit: ContentUnit, index: int | None = None):
        """
        插入内容单元到上下文列表中

        :param content_unit: 内容单元
        :param index: 插入位置，默认为None，表示插入到末尾
        """
        if index is None:
            self.context_list.append(content_unit)
        elif abs(index) <= len(self.context_list):
            raise IndexError("Index out of range")
        else:
            self.context_list.insert(index, content_unit)
        return self
    
    @property
    def last_content(self) -> ContentUnit:
        """
        获取最后一个上下文单元
        """
        if not self.context_list:
            self.context_list.append(ContentUnit())
        return self.context_list[-1]
    
    def append(self, content: ContentUnit) -> None:
        """
        添加上下文单元
        """
        self.context_list.append(content)
    
    def append_content(
        self,
        reasoning_content:str = "",
        content: str = "",
        role: ContextRole = ContextRole.USER,
        role_name: str |  None = None,
        is_prefix: bool | None = None,
        funcResponse: CallingFunctionResponse | None = None,
        tool_call_id: str = "",
    ):
        """
        添加上下文内容

        :param reasoning_content: Resoning 内容
        :param content: 内容
        :param role: 角色
        :param role_name: 角色名称
        :param is_prefix: 是否为前缀(用于提交给模型用于续写)
        :param funcResponse: 函数响应
        :param tool_call_id: 工具调用ID
        """
        self.append(ContentUnit(
            reasoning_content = reasoning_content,
            content = content,
            role = role,
            role_name = role_name,
            prefix = is_prefix,
            funcResponse = funcResponse,
            tool_call_id = tool_call_id,
        ))
    
    def pop(self, index: int = -1) -> ContentUnit:
        """
        弹出一个上下文单元

        :param index: 弹出第几个上下文单元，默认为最后一个
        :return: 弹出的上下文单元
        :raises IndexOutOfRangeError: 如果index超出范围，则抛出该异常
        """
        if index not in range(-len(self.context_list), len(self.context_list)):
            raise IndexOutOfRangeError("index out of range")
        return self.context_list.pop(index)
    
    def pop_last_n(self, n: int) -> ContextObject:
        """
        弹出最后n个上下文单元

        :param n: 弹出的元素个数
        :return: 弹出的元素列表
        :raises IndexOutOfRangeError: 数量超出范围
        """
        if n not in range(0, len(self.context_list)):
            raise IndexOutOfRangeError("index out of range")
        pop_list:list[ContentUnit] = []
        for _ in range(n):
            pop_list.append(self.pop())
        return ContextObject(
            prompt = self.prompt,
            context_list = pop_list
        )
    
    def pop_begin_n(self, n: int = 0) -> ContentUnit:
        """
        弹出头部的n个元素

        :param n: 弹出的元素个数
        :return: 弹出的元素列表
        :raise IndexOutOfRangeError: 数量超出范围
        """
        if n not in range(0, len(self.context_list)):
            raise IndexOutOfRangeError("index out of range")
        pop_list = self.context_list[:n]
        self.context_list = self.context_list[n:]
        return pop_list
    
    @property
    def is_empty(self) -> bool:
        """
        判断上下文是否为空
        """
        return not self.prompt and not self.context_list
    
    @property
    def has_new_func_calling_response(self) -> bool:
        """
        判断上下文是否包含新的函数调用响应
        """
        return self.last_content.funcResponse is not None
    
    def shrink(self, length: int, ensure_role_at_top: ContextRole = ContextRole.USER):
        """
        缩小上下文长度
        
        :param length: 上下文总字数
        :param ensure_role_at_top: 确保指定角色在顶部
        :raise IndexOutOfRangeError: 数量超出范围
        """
        if length < 0:
            raise IndexOutOfRangeError("length must be positive")

        # 当length大于等于实际长度时，不做任何事
        if abs(length) >= self.total_length:
            return
        
        while self.total_length > length:
            self.pop_begin_n(1)
        
        if self.context_list and self.context_list[0].role != ensure_role_at_top:
            # 从头部寻找第一个为ensure_role_at_top的ContextUnit
            for i in range(len(self.context_list)):
                if self.context_list[i].role == ensure_role_at_top:
                    self.context_list = self.context_list[i:]
                    break
            else:
                raise IndexOutOfRangeError(f"Role {ensure_role_at_top} not found in context_list")
        
    def copy(self) -> ContextObject:
        """
        复制对象
        :return: 复制后的对象
        """
        return ContextObject(
            prompt = self.prompt,
            context_list = self.context_list.copy(),
        )
    
    @classmethod
    def from_context(cls, context: list[dict]) -> ContextObject:
        """
        从上下文列表构建对象
        
        :param context: 上下文列表
        :return: 构建的对象
        """
        contextObj = cls()
        contextObj.context_list = []
        for content in context:
            contextObj.context_list.append(ContentUnit().from_content(content))
        return contextObj
        