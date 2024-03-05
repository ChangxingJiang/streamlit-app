"""
Streamlit 应用页面
"""

import abc


class StreamlitPage(abc.ABC):
    """Streamlit 应用页面"""

    @staticmethod
    @abc.abstractmethod
    def page_name() -> str:
        """当前页面的名称"""

    @abc.abstractmethod
    def draw_page(self) -> None:
        """绘制 streamlit 页面

        在 draw_page 方法中构造 streamlit 页面
        """
