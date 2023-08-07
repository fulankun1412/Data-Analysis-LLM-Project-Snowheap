from common.streamlitCommon import BaseInterface

import streamlit as st
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker
import pandas as pd
from pandasai import PandasAI
from langchain.llms import OpenAI

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
    def __init__(self, apiKey) -> None:
        self.apiKey = apiKey

    def LLM_OpenAi(self, prompt):
        llm = OpenAI(openai_api_key=self.apiKey)
        return llm.predict(prompt)
class HomeInterface(BaseInterface):
    def __init__(self) -> None:
        pass
    
    def userInteraction(self):
        dataSource = DataSource()
        st.text("Selected table, showing first five of data:")
        dfShow = st.empty()
        st.divider()
        
        col1, col2 = st.columns(spec=[0.5, 0.5], gap="medium")
        with col1:
            selectedSourceTable = st.selectbox(label="Select data source table:", options=dataSource.table_list)
        with col2:
            uploadedDocument = st.file_uploader(label="Upload your document:", )
        dfShow.dataframe(data=DataSource().getHeadData(selectedSourceTable), use_container_width=True)
        promptText = st.text_area(label="Input your prompt:")
        apiKey = st.text_input(label="Input your OpenAI API key:")

        if st.button("Get Answer"):
            llm = LLM(apiKey=apiKey)
            pred = llm.LLM_OpenAi(prompt=promptText)

            st.markdown(f"""
                        <p style="text-align: justify;">
                        {pred}
                        </p>
                        """, unsafe_allow_html=True)
            

    def main(self):
        st.title("Data Analyst Assistant")
        self.sideBar()
        
        self.userInteraction()

if __name__ == "__main__":
    HomeInterface().main()