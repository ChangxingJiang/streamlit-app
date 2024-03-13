"""
Streamlit 应用
"""

import inspect
import os
import sys
from typing import List, Optional, Type, Dict, Any

import streamlit.web.cli

from streamlit_app.errors import StreamlitAppDeployError
from streamlit_app.page import StreamlitPage
from streamlit_app.utils import clear_folder, get_import_name_by_file_path


class PageInfo:
    """页面信息"""

    def __init__(self, name: str, page_class: Type[StreamlitPage], params: Dict[str, Any]):
        self._name = name
        self._page_class = page_class
        self._params = params

    @property
    def name(self) -> str:
        return self._name

    @property
    def page_class(self) -> Type[StreamlitPage]:
        return self._page_class

    @property
    def params(self) -> Dict[str, Any]:
        return self._params

    def __repr__(self) -> str:
        return f"PageInfo[name={self.name}, page_class={self.page_class.__name__}, params={self.params}]"


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

        self.main_page: Optional[PageInfo] = None
        self.pages: List[PageInfo] = []

        self.is_deploy: bool = False

    def set_main_page(self, page: Type[StreamlitPage], params: Optional[Dict[str, Any]] = None) -> None:
        """设置主页面，如已经设置主页面则覆盖它

        Parameters
        ----------
        page : Type[StreamlitPage]
            主页面类
        params : Optional[Dict[str, Any]], default = None
            主页面类初始化时的参数
        """
        if params is None:
            params = {}
        assert issubclass(page, StreamlitPage), f"page.__name__={page.__name__}"
        self.main_page = PageInfo(page(params=params).page_name(), page, params)

    def append_page(self, page: Type[StreamlitPage], params: Optional[Dict[str, Any]] = None) -> None:
        """添加其他页面

        Parameters
        ----------
        page : Type[StreamlitPage]
            其他页面类
        params : Optional[Dict[str, Any]], default = None
            主页面类初始化时的参数
        """
        if params is None:
            params = {}
        assert issubclass(page, StreamlitPage), f"page.__class__.__name__={page.__class__.__name__}"
        self.pages.append(PageInfo(page(params=params).page_name(), page, params))

    def deploy(self) -> None:
        """部署 Streamlit 应用服务"""
        # 检查是否设置了主页面
        if self.main_page is None:
            raise StreamlitAppDeployError("未定义主页面")

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
        self._deploy_page(self.main_page, os.path.join(self.deploy_dir, f"{self.main_page.name}.py"))

        # 创建 pages 文件夹
        os.mkdir(os.path.join(self.deploy_dir, "pages"))

        # 部署其他页面
        for page in self.pages:
            self._deploy_page(page, os.path.join(self.deploy_dir, "pages", f"{page.name}.py"))

    @staticmethod
    def _deploy_page(page: PageInfo, file_path: str):
        """部署 1 个页面"""
        # 获取类的基本信息
        class_name = page.page_class.__name__
        module_path = get_import_name_by_file_path(inspect.getsourcefile(page.page_class))

        # 创建页面文件
        with open(file_path, "w", encoding="UTF-8") as file:
            file.write(f"from {module_path} import {class_name} \n"
                       f"\n"
                       f"{class_name}(params={page.params}).draw_page()")
        print(f"[Deployment] 部署完成: {page}")

    def start(self):
        """启动 Streamlit 应用服务"""
        # 将首页添加到配置信息中
        if len(sys.argv) > 1:
            sys.argv = sys.argv[:1]
        sys.argv.append(os.path.join(self.deploy_dir, f"{self.main_page.name}.py"))

        # 启动 streamlit
        streamlit.web.cli.main_run()

    def deploy_and_start(self):
        """部署并启动 Streamlit 应用服务"""
        self.deploy()
        self.start()
