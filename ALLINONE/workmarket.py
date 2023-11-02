from PIL import Image
import streamlit as st
from langchain.agents import *
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.sql_database import SQLDatabase
from langchain.chat_models import ChatOpenAI


def main():
    load_dotenv()
    st.set_page_config(page_title="query database for workmarket")
    st.header("Query the Data Base")
    db_user = "root"
    db_password = ""
    db_host = "localhost"
    db_name = "test"
    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")
    toolkit = SQLDatabaseToolkit(db=db, llm=OpenAI(temperature=0))
    agent_executor = create_sql_agent(
    llm=OpenAI(temperature=0),
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )

    user_question = st.text_input(" please a ask query")

    if user_question is not None and user_question != "":
            with st.spinner(text="In Progress..."):
                st.write(agent_executor.run(user_question)
)

if _name_ == "__main__":
    main()