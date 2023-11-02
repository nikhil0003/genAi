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
        #iconimg= Image.open('workmarket.png')
        st.set_page_config(page_title="WorkMarket ZenDesk ", layout="wide")
        #st.image(iconimg)
        st.title("WorkMarket MySql DataBase Powder by GENAI")
        db_user = "root"
        db_password = "admin"
        db_host = "localhost"
        db_name = "test"
        db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")

        template = """
        You are an agent designed to interact with a SQL database.Given an input question, create a syntactically correct mysql query to run, then look at the results of the query and return the answer.Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 10 results.
        You can order the results by a relevant column to return the most interesting examples in the database.
        Never query for all the columns from a specific table, only ask for the relevant columns given the question.
        You have access to tools for interacting with the database.
        Only use the below tools. Only use the information returned by the below tools to construct your final answer.
        You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

        DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

        If the question does not seem related to the database, just return "Please contact workmarket support ,I don't know" as the answer.

        

        sql_db_query: Input to this tool is a detailed and correct SQL query, output is a result from the database. If the query is not correct, an error message will be returned. If an error is returned, rewrite the query, check the query, and try again. If you encounter an issue with Unknown column 'xxxx' in 'field list', using sql_db_schema to query the correct table fields.
        sql_db_schema: Input to this tool is a comma-separated list of tables, output is the schema and sample rows for those tables. Be sure that the tables actually exist by calling sql_db_list_tables first! Example Input: 'table1, table2, table3'
        sql_db_list_tables: Input is an empty string, output is a comma separated list of tables in the database.
        sql_db_query_checker: Use this tool to double check if your query is correct before executing it. Always use this tool before executing a query with sql_db_query!

        Use the following format:

        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [sql_db_query, sql_db_schema, sql_db_list_tables, sql_db_query_checker]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question

        Begin!

        Question: {input}
        Thought: I should look at the tables in the database to see what I can query.  Then I should query the schema of the most relevant tables.
        {agent_scratchpad}
        """
        
        
        llm=ChatOpenAI(temperature=0)
        toolkit = SQLDatabaseToolkit(db=db,llm=llm)

        agent_executor = create_sql_agent(
        llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        )
        user_question = st.text_input("Please a Ask Query")
        if user_question is not None and user_question != "":
            with st.spinner(text="In progress..."):
                result = agent_executor.run(user_question)
                print(result)
                st.write(result)


if __name__ == "__main__":
    main()
