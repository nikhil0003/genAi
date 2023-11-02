from langchain.agents import initialize_agent, AgentType, Tool, create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from dotenv import load_dotenv
from langchain.sql_database import SQLDatabase
from langchain.chat_models import ChatOpenAI
#from langchain.prompts import ChatPromptTemplate
import streamlit as st

import langchain


def main():
    st.title('Uber pickups in NYC')
    print("hello")
    langchain.debug = True
    load_dotenv()

    db_user = "root"
    db_password = "admin"
    db_host = "localhost"
    db_name = "test"
    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")
    llm = ChatOpenAI(temperature=0)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent_executor = create_sql_agent(
        llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        handle_parsing_errors="Invalid input , please provide proper input",
    )
    result = agent_executor.run("how many records are their")
    print(result)
    st.write(result)


if __name__ == "main":
    main()
