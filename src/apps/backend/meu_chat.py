import os
import datetime
import streamlit as st

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage, AIMessage


from enum import Enum
from backend.database import Chat


def find_model(model: str):
    model = model.lower()

    if model in ("llama3-8b-8192", "llama-3.1-8b-instant"):
        return ChatGroq(model=model, temperature=0, api_key=os.getenv("GROQ_API_KEY"))

    if model in ("gpt-3.5-turbo", "gpt-4o"):
        return ChatOpenAI(
            model=model, temperature=0, api_key=os.getenv("OPENAI_API_KEY")
        )
    return "Modelo não cadastrado :("


models = [
    "LLAMA-3.1-8B-INSTANT",
    "LLAMA3-8B-8192",
    "GPT-3.5-TURBO",
    "GPT-4o",
]


def upsert_chat(chat_id, messages):
    if chat_id:
        return Chat.update(history=messages, updated_at=datetime.now()).where(
            Chat.id == chat_id
        )

    chat = Chat(
        name=messages[0]["content"][:30],
        history=messages,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    chat.save()
    st.session_state.chat_id = chat.id
    return chat.id


def get_session_history(session_id):
    return SQLChatMessageHistory(session_id, "sqlite:///memory.db")

model = st.session_state["model"] or find_model("LLAMA-3.1-8B-INSTANT")

with_message_history = RunnableWithMessageHistory(
    st.session_state["model"], get_session_history
)


def send_message(message: str):
    stream = with_message_history.stream(
        [HumanMessage(content=message)],
        config={"configurable": {"session_id": st.session_state["session_id"]}},
    )
    
    return stream


# history = get_session_history(st.session_state["session_id"])
history = get_session_history("abc2")
