# Streamlit 的对象化处理工具

Streamlit-App 通过根据在部署目录自动创建满足 streamlit 多页面要求的 py 脚本的方法，实现了对象化创建 streamlit 服务的功能。

## 安装

```bash
pip install streamlit-app
```

## 使用

```python
import streamlit as st

from streamlit_app import Application, StreamlitPage


class MyMainPage(StreamlitPage):

    def page_name(self) -> str:
        return self.params.get("name")

    def draw_page(self) -> None:
        st.title("Main Page Title")
        st.write("streamlit-app app page test")


class MySubPage(StreamlitPage):

    def page_name(self) -> str:
        return "test_sub_page"

    def draw_page(self) -> None:
        st.title("Sub Page Title")
        st.write("streamlit-app sub page test")


if __name__ == "__main__":
    application = Application()
    application.set_main_page(MyMainPage, params={"name": "Main Page Title"})
    application.append_page(MySubPage)
    application.deploy_and_start()
```

实例化 `StreamlitPage.Application` 类，调用 `set_main_page()` 方法设置主页面，使用 `append_page()` 方法设置其他页面，在设置完成后，调用 `deploy_and_start()` 方法部署并启动 Streamlit 服务。

## 修改记录

##### 0.0.3

- 新增：根据调用栈自动计算组件的唯一键的工具
- 修复：修复不同路径下 py 脚本文件名相同无法正常展示的 Bug

##### 0.0.2

- 新增：支持在初始化 StreamPage 时添加参数，将 StreamPage 的静态方法改为非静态方法

##### 0.0.1：初始化