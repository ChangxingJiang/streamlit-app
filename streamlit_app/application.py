"""
Streamlit 应用
"""

import inspect
import os
import sys
from typing import List, Optional, Type

import streamlit.web.cli

from streamlit_app.errors import StreamlitAppDeployError
from streamlit_app.page import StreamlitPage


class Application:
    """Streamlit 应用"""

    def __init__(self, deploy_dir: Optional[str] = None, auto_clear_deploy_dir: bool = True):
        """Streamlit 应用的构造方法

        Parameters
        ----------
        deploy_dir : Optional[str], default = None
            部署文件夹路径，如果为 None 则部署在当前入口脚本目录下的 .deploy 文件夹中
        auto_clear_deploy_dir : bool, default = True
            是否自动清空部署目录并重新部署
        """
        if deploy_dir is None:  # 没有指定部署路径，则使用默认路径
            deploy_dir = os.path.join(os.getcwd(), ".deploy")  # 获取当前入口脚本路径下的 .deploy 文件夹
            if not os.path.exists(deploy_dir):
                os.mkdir(deploy_dir)  # 如果目录不存在则创建

        self.deploy_dir = deploy_dir
        self.auto_clear_deploy_dir = auto_clear_deploy_dir

        self.main_page: Optional[Type[StreamlitPage]] = None
        self.pages: List[Type[StreamlitPage]] = []

        self.is_deploy: bool = False

    def set_main_page(self, page: Type[StreamlitPage]) -> None:
        """设置主页面，如已经设置主页面则覆盖它

        Parameters
        ----------
        page : Type[StreamlitPage]
            主页面类
        """
        self.main_page = page

    def append_page(self, page: Type[StreamlitPage]) -> None:
        """添加其他页面

        Parameters
        ----------
        page : Type[StreamlitPage]
            其他页面类
        """
        self.pages.append(page)

    def deploy(self) -> None:
        """部署 Streamlit 应用服务"""
        # 检查是否设置了主页面
        if self.main_page is None:
            raise StreamlitAppDeployError("未定义主页面")

        # 检查主页面和子页面是否为 StreamlitPage 的子类
        if not issubclass(self.main_page, StreamlitPage):
            raise StreamlitAppDeployError(f"{self.main_page.__name__} 不是 StreamlitPage 的子类")
        for page in self.pages:
            if not issubclass(page, StreamlitPage):
                raise StreamlitAppDeployError(f"{page.__name__} 不是 StreamlitPage 的子类")

        # 检查主页面和子页面的 main_page 方法是否为静态方法
        if self.main_page.page_name.__code__.co_argcount != 0:
            raise StreamlitAppDeployError(f"{self.main_page.__name__}.page_name() 不是静态方法")
        for page in self.pages:
            if page.page_name.__code__.co_argcount != 0:
                raise StreamlitAppDeployError(f"{page.__name__}.page_name() 不是静态方法")

        # 检查部署路径
        if not os.path.isdir(self.deploy_dir):
            raise StreamlitAppDeployError(f"部署路径不是文件夹: {self.deploy_dir}")
        if os.listdir(self.deploy_dir):
            if self.auto_clear_deploy_dir is True:
                clear_folder(self.deploy_dir)
            else:
                raise StreamlitAppDeployError(f"部署路径不为空: {self.deploy_dir}")

        print(f"Streamlit 环境部署位置: {self.deploy_dir}")

        # 部署主页面
        self._deploy_page(self.main_page, os.path.join(self.deploy_dir, f"{self.main_page.page_name()}.py"))

        # 创建 pages 文件夹
        os.mkdir(os.path.join(self.deploy_dir, "pages"))

        # 部署其他页面
        for page in self.pages:
            self._deploy_page(page, os.path.join(self.deploy_dir, "pages", f"{page.page_name()}.py"))

    @staticmethod
    def _deploy_page(page_class: Type[StreamlitPage], file_path: str):
        """部署 1 个页面"""

        # 获取类的基本信息
        class_path = inspect.getsourcefile(page_class)
        class_dir_path = os.path.dirname(class_path)
        class_file_name = os.path.basename(class_path).replace(".py", "")
        class_name = page_class.__name__

        # 将文件夹添加到环境变量
        sys.path.append(class_dir_path)

        # 创建页面文件
        with open(file_path, "w", encoding="UTF-8") as file:
            file.write(f"from {class_file_name} import {class_name} \n"
                       f"\n"
                       f"{class_name}().draw_page()")

    def start(self):
        """启动 Streamlit 应用服务"""
        # 将首页添加到配置信息中
        if len(sys.argv) > 1:
            sys.argv[1] = os.path.join(self.deploy_dir, f"{self.main_page.page_name()}.py")
        else:
            sys.argv.append(os.path.join(self.deploy_dir, f"{self.main_page.page_name()}.py"))

        # 启动 streamlit
        streamlit.web.cli.main_run()

    def deploy_and_start(self):
        """部署并启动 Streamlit 应用服务"""
        self.deploy()
        self.start()


def clear_folder(folder_path: str) -> None:
    """清空文件夹

    Parameters
    ----------
    folder_path : str
        文件夹的路径
    """
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
        else:
            clear_folder(file_path)
            os.rmdir(file_path)
