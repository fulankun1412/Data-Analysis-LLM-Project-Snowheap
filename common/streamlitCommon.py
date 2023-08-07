import streamlit as st

class BaseInterface:
    def __init__(self) -> None:
        pass

    def sideBar(self):
        with st.sidebar:
            st.image("./static/snowheap-icon.jpeg")