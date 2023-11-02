from PIL import Image
import streamlit as st
from dotenv import load_dotenv
from customWorkmarketAgent import create_sql_agent_custom
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.sql_database import SQLDatabase
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from workMarketprompt import PREFIX,SUFFIX
from langchain.schema.messages import AIMessage, SystemMessage,HumanMessage
import langchain



def main():
        #langchain.debug = True
        load_dotenv()
        iconimg= Image.open('workmarket.png')
        st.set_page_config(page_title="WorkMarket ZenDesk ", page_icon=iconimg, layout="wide")
        st.image(iconimg)
        st.title("WorkMarket MySql DataBase by GENAI")
        db_user = "root"
        db_password = ""
        db_host = "localhost"
        db_name = "gen_ai"
        db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")
        
        llm=ChatOpenAI(temperature=0)
        toolkit = SQLDatabaseToolkit(db=db,llm=llm)
        
        chathistory=[]
        systemmsg=PREFIX
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []

        user_question = st.text_input("Please a Ask Query")
        if user_question is not None and user_question != "":
            with st.spinner(text="In progress..."):
                print(chathistory)
                if "chat_history"  in st.session_state:
                    for message in st.session_state.chat_history:
                        if(message["role"]=='user'):
                            chathistory.append('Human:'+ message["content"])
                        if(message["role"]=='assistant'):
                            chathistory.append('AI:'+ message["content"])
                    print(st.session_state.chat_history)
                    if(len(chathistory)>0):
                        temp=""""""
                        for i in chathistory:
                            temp=temp+"\n"+i
                        systemmsg = systemmsg+"""
                        Previous Coversation history :
                        """+temp
                messages = [
                SystemMessage(content=systemmsg),
                HumanMessagePromptTemplate.from_template("{input}"),
                AIMessage(content=SUFFIX),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
                ]

                agent_executor = create_sql_agent_custom(
                llm,
                toolkit=toolkit,
                verbose=True,
                agent_type=AgentType.OPENAI_FUNCTIONS,
                max_iterations=30,
                messages=messages,
                chatHistory=chathistory
                )
                result = agent_executor.run(user_question)
                st.session_state["chat_history"].append(
                     {
                      "role": "user", 
                      "content": user_question
                     })
                st.session_state["chat_history"].append(
                     {
                        "role": "assistant", 
                         "content": result
                     })
        
        for message in st.session_state.chat_history:
             st.chat_message(message["role"]).write(message["content"])

if __name__ == "__main__":
    main()