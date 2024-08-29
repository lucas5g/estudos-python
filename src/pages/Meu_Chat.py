import streamlit as st
import os
import time
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from peewee import SqliteDatabase, Model, CharField, DateTimeField, IntegerField


def get_session_history(session_id):
    return SQLChatMessageHistory(session_id, "sqlite:///memory.db")


# init
def init():
    st.set_page_config(
        page_title="Meu Chat", page_icon=":left_speech_bubble:", layout="wide"
    )

    if "session_id" not in st.session_state:
        st.session_state.session_id = int(time.time())


def find_model(model: str):
    model = model.lower()

    if model in ("llama3-8b-8192", "llama-3.1-8b-instant"):
        return ChatGroq(model=model, temperature=0, api_key=os.getenv("GROQ_API_KEY"))

    if model in ("gpt-3.5-turbo", "gpt-4o"):
        return ChatOpenAI(
            model=model, temperature=0, api_key=os.getenv("OPENAI_API_KEY")
        )
    return "Modelo não cadastrado :("


def main():

    model_name = st.selectbox(
        "Modelos",
        [
            "LLAMA-3.1-8B-INSTANT",
            "LLAMA3-8B-8192",
            "GPT-3.5-TURBO",
            "GPT-4o",
        ],
    )

    st.markdown(
        f"""
        ## Meu Chat {model_name}
        """
    )

    with_message_history = RunnableWithMessageHistory(
        find_model(model_name), get_session_history
    )

    st.write(st.session_state)

    history = get_session_history(st.session_state["session_id"])

    for message in history.messages:
        if isinstance(message, HumanMessage):
            st.chat_message("user").markdown(message.content)
        elif isinstance(message, AIMessage):
            st.chat_message("assistant").markdown(message.content)

    prompt = st.chat_input("Mensagem Meu Chat")

    if prompt:
        st.chat_message("user").markdown(prompt)

        stream = with_message_history.stream(
            [HumanMessage(content=prompt)],
            config={"configurable": {"session_id": st.session_state["session_id"]}},
        )

        st.chat_message("assistant").write_stream(stream)


init()
main()


# def select_chat(chat_id: int):
#     st.session_state.chat_id = chat_id

#     if not chat_id:
#         st.session_state.messages = []
#         return

#     chat = Chat.get_by_id(chat_id)
#     st.session_state.messages = ast.literal_eval(chat.history)


with st.sidebar:
    st.button("Nova Mensagem", use_container_width=True)

    db = SqliteDatabase("memory.db")

    class Message(Model):
        session_id = IntegerField()
        message = CharField()

        class Meta:
            database = db
            table_name = "message_store"

    db.connect()

    messages = Message.select(Message.session_id, Message.message).distinct()

    for message in messages:
        st.write(message.message)
        # st.button(label=str(message.message), use_container_width=True)
