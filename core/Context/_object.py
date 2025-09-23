from dataclasses import dataclass, field
from typing import overload
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
        if self.reasoning_content:
            return len(self.reasoning_content)
        else:
            return len(self.content)
    
    def update_from_content(self, content: dict) -> None:
        """
        更新上下文内容
        :param content: 上下文内容
        :return:
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
    @property
    def as_content(self) -> list[dict]:
        """
        OpenAI Message兼容格式列表单元
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
                if self.reasoning_content:
                    assistant_content["reasoning_content"] = self.reasoning_content
                if self.funcResponse:
                    assistant_content["tool_calls"] = self.funcResponse.as_content
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
    def __getitem__(self, index: slice) -> "ContextObject":
        ...
    
    def __getitem__(self, index: int | slice):
        if isinstance(index, int):
            return self.context_list[index]
        elif isinstance(index, slice):
            return ContextObject(prompt=self.prompt, context_list=self.context_list[index])
        else:
            raise TypeError("index must be int or slice")
    
    def __setitem__(self, index: int, value: ContentUnit):
        self.context_list[index] = value

    def __len__(self):
        return len(self.context_list)
    
    def __iter__(self):
        # 先 yield 提示词
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
    def total_length(self) -> int:
        """
        获取上下文总长度
        
        :return: 上下文总长度
        """
        return sum([len(content) for content in self.context_list]) + (len(self.prompt) if self.prompt else 0)

    @property
    def context(self) -> list[dict]:
        """
        获取上下文
        """
        context_list = []
        if self.context_list:
            for content in self.context_list:
                context_list += content.as_content
        return context_list
    
    @property
    def full_context(self) -> list[dict]:
        """
        获取上下文，如果有提示词，则添加到最前面
        """
        context_list = self.context
        if self.prompt:
            context_list = self.prompt.as_content + context_list
        return context_list
    
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
        prefix: bool | None = None,
        funcResponse: CallingFunctionResponse | None = None,
        tool_call_id: str = "",
    ):
        """
        添加上下文内容
        """
        self.append(ContentUnit(
            reasoning_content=reasoning_content,
            content=content,
            role=role,
            role_name=role_name,
            prefix=prefix,
            funcResponse=funcResponse,
            tool_call_id=tool_call_id,
        ))
    
    def pop(self, index: int = -1) -> ContentUnit:
        """
        弹出最后一个上下文单元
        """
        return self.context_list.pop(index)
    
    def pop_last_n(self, n: int) -> "ContextObject":
        """
        弹出最后n个上下文单元
        """
        pop_list:list[ContentUnit] = []
        for _ in range(n):
            pop_list.append(self.pop())
        return ContextObject(prompt=self.prompt, context_list=pop_list)
    
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
    
    @classmethod
    def from_context(cls, context: list[dict]) -> "ContextObject":
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