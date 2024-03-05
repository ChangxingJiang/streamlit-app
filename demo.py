import streamlit as st

from streamlit_app import Application, StreamlitPage


class MyMainPage(StreamlitPage):

    @staticmethod
    def page_name() -> str:
        return "test_main_page"

    def draw_page(self) -> None:
        st.title("Main Page Title")
        st.write("streamlit-app app page test")


class MySubPage(StreamlitPage):

    @staticmethod
    def page_name() -> str:
        return "test_sub_page"

    def draw_page(self) -> None:
        st.title("Sub Page Title")
        st.write("streamlit-app sub page test")


if __name__ == "__main__":
    application = Application()
    application.set_main_page(MyMainPage)
    application.append_page(MySubPage)
    application.deploy_and_start()
