from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.schema import HumanMessage, AIMessage

from langchain.agents.agent_types import AgentType

from langchain.chains import LLMMathChain

# from langchain.utilities import SerpAPIWrapper
from langchain_community.utilities import SerpAPIWrapper
from langchain.agents import (
    initialize_agent,
    Tool,
    create_structured_chat_agent,
    create_openai_functions_agent,
)

# create_openai_functions_agent, create_react_agent,
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from utils.model import model
import streamlit as st
from dotenv import load_dotenv

import os

load_dotenv()

db = SQLDatabase.from_uri("sqlite:///Chinook.db")


db_chain = SQLDatabaseChain.from_llm(model, db, verbose=True)
llm_math_chain = LLMMathChain.from_llm(model, verbose=True)
search = SerpAPIWrapper(serpapi_api_key=os.getenv("SERPAPI_API_KEY"))


tools = [
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events. You should ask targeted questions",
    ),
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="useful for when you need to answer questions about math.",
    ),
    Tool(
        name="FooBar-DB",
        func=db_chain.invoke,
        description="useful for when you need to answer questions about FooBar. Input should be in the form of a question containing full context",
    ),
]

memory = ConversationBufferMemory(memory_key="memory", return_messages=True)

agent_kwargs = {"extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")]}

agent = initialize_agent(
    tools,
    llm=model,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
    agent_kwargs=agent_kwargs,
    memory=memory,
)

prompt = hub.pull("hwchase17/openai-functions-agent")


def handle_chat(query):
    response = agent.run(query)
    return response


if "history" not in st.session_state:
    st.session_state["history"] = []

st.title("AI Chatbot")


def send_message():
    if st.session_state.user_input:
        user_message = st.session_state.user_input
        res = handle_chat(user_message)
        st.session_state["history"].append(("You", user_message))
        st.session_state["history"].append(("AI", res))
        st.session_state.user_input = ""


for idx, (user, message) in enumerate(st.session_state["history"]):
    if user == "You":
        st.text_area(f"Você: {idx+1}", message, key=f"msg{idx}u", disabled=True)
    else:
        st.text_area(f"AI: {idx+1}", message, key=f"msg{idx}b", disabled=True)

st.markdown("---")

user_input = st.text_input(
    "Entre com sua mensagem", key="user_input", on_change=send_message
)

send_button = st.button("Enviar")

if send_button and st.session_state.user_input:
    send_message()
