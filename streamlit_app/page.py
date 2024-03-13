"""
Streamlit 应用页面
"""

import abc
import inspect
from typing import Dict, Any


class StreamlitPage(abc.ABC):
    """Streamlit 应用页面"""

    def __init__(self, params: Dict[str, Any]):
        self._params = params
        print(f"[streamlit-app] 正在初始化: {self.__class__.__name__}, params={self._params}")

    @property
    def params(self) -> Dict[str, Any]:
        return self._params

    @staticmethod
    @abc.abstractmethod
    def page_name() -> str:
        """当前页面的名称"""

    @abc.abstractmethod
    def draw_page(self) -> None:
        """绘制 streamlit 页面

        在 draw_page 方法中构造 streamlit 页面
        """

    @staticmethod
    def get_streamlit_default_key() -> str:
        """Streamlit 的 key 自动分配器：根据调用路径构造，理论上不存在同名的情况"""
        stack_list = []
        frame = inspect.currentframe()
        while frame.f_back:
            if frame.f_back.f_code.co_name == "_run_script":  # 如果已经追溯到 _run_script，则不再继续递归栈信息
                break
            stack_list.append(f"{frame.f_back.f_code.co_name}:{frame.f_back.f_lineno}")
            frame = frame.f_back
        return "-".join(reversed(stack_list))  # 根据调用链路，获取 _run_script 函数之后的唯一键
