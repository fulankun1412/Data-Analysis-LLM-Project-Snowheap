from common import BaseInterface

import streamlit as st
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker
import pandas as pd
from pandasai import PandasAI

class DataSource:
    def __init__(self) -> None:
        DATABASE_URL = "sqlite:///datasets.db"
        self.engine = create_engine(DATABASE_URL)

        metadata = MetaData()
        metadata.reflect(bind=self.engine)

        self.table_list = list(metadata.tables.keys())
        
    def getData(self, SELECTED_TABLE):
        Session = sessionmaker(bind=self.engine)
        session = Session()

        selected_table = text(f"SELECT * FROM {SELECTED_TABLE}")

        result = session.execute(selected_table).fetchall()
        return pd.DataFrame(result)

    def getHeadData(self, SELECTED_TABLE):
        return self.getData(SELECTED_TABLE).head(5)
    
class LLM:
    def __init__(self) -> None:
        pass


class HomeInterface(BaseInterface):
    def __init__(self) -> None:
        pass
    
    def userInput(self):
        dataSource = DataSource()
        dfShow = st.empty()
        col1, col2 = st.columns(spec=[0.7, 0.3], gap="medium")
        with col1:
            promptText = st.text_area(label="Input your Prompt:")
        with col2:
            selectedSource = st.selectbox(label="Select data source Table:", options=dataSource.table_list)
        
        st.dataframe(data=DataSource().getHeadData(selectedSource), use_container_width=True)

    def main(self):
        st.title("Data Analyst Assistant")
        self.sideBar()
        with st.container():
            self.userInput()

if __name__ == "__main__":
    HomeInterface().main()