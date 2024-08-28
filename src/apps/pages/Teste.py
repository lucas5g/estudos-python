import streamlit as st 

from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-3.5-turbo")

def get_session_history(session_id):
    return SQLChatMessageHistory(session_id, "sqlite:///memory.db")

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables.history import RunnableWithMessageHistory


with_message_history = RunnableWithMessageHistory(model, get_session_history)

config = {"configurable": {"session_id": "abc2"}}

# response = with_message_history.invoke(
#     [HumanMessage(content="Ola")],
#     config=config,
# )

# response.content

history = get_session_history("abc2")

for message in history.messages:
    if isinstance(message, HumanMessage):
        st.chat_message("user").markdown(message.content)
    elif isinstance(message, AIMessage):
        st.chat_message("assistant").markdown(message.content)