from common import BaseInterface
import streamlit as st

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.engine.url import make_url

DATABASE_URL = "sqlite:///datasets.db"
engine = create_engine(DATABASE_URL)

metadata = MetaData()
metadata.reflect(bind=engine)

table_list = list(metadata.tables.keys())

class HomeInterface(BaseInterface):
    def __init__(self) -> None:
        pass

    def userInput(self):
        col1, col2 = st.columns(spec=[0.7, 0.2], gap="medium")
        with col1:
            promptText = st.text_area(label="Input your Prompt:")
        with col2:
            dataSource = st.selectbox(label="Select data source Table:", options=table_list)

    def main(self):
        self.sideBar()
        with st.container():
            self.userInput()

if __name__ == "__main__":
    HomeInterface().main()