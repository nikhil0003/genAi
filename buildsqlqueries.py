from PIL import Image
import streamlit as st
from dotenv import load_dotenv
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.sql_database import SQLDatabase
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document
from langchain.agents.agent_toolkits import create_retriever_tool


def main():
        load_dotenv()
        iconimg= Image.open('workmarket.png')
        st.set_page_config(page_title="WorkMarket ZenDesk ", page_icon=iconimg, layout="wide")
        st.image(iconimg)
        st.title("WorkMarket MySql DataBase Powder by GENAI")
        db_user = "root"
        db_password = ""
        db_host = "localhost"
        db_name = "gen_ai"
        db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")
        
        
        llm=ChatOpenAI(temperature=0)
        toolkit = SQLDatabaseToolkit(db=db,llm=llm)

        agent_executor = create_sql_agent(
        llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        )
        user_question = st.text_input("Please a Ask Query")
        if user_question is not None and user_question != "":
            with st.spinner(text="In progress..."):
                result = agent_executor.run(user_question)
                print(result)
                st.write(result)


if __name__ == "__main__":
    main()