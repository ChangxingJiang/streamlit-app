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
