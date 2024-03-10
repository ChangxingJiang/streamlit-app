"""
Streamlit 应用页面
"""

import abc
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
