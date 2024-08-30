import os
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_groq import ChatGroq
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from sqlalchemy import create_engine
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from database import Chat

def get_session_history(session_id):
    print(session_id)
    return Chat.get(Chat.id == session_id)


# def get_session_history(session_id):
#     return SQLChatMessageHistory(session_id, 'sqlite:///memory.db')


def find_model(model: str):
    model = model.lower()

    if model in ("llama3-8b-8192", "llama-3.1-8b-instant"):
        return ChatGroq(model=model, temperature=0, api_key=os.getenv("GROQ_API_KEY"))

    if model in ("gpt-3.5-turbo", "gpt-4o"):
        return ChatOpenAI(
            model=model, temperature=0, api_key=os.getenv("OPENAI_API_KEY")
        )
    return "Modelo não cadastrado :("


def send_message(model_name, message, session_id):

    model = find_model(model_name)

    with_message_history = RunnableWithMessageHistory(
        model,
        get_session_history,
    )

    return with_message_history.stream(
        [HumanMessage(content=message)],
        config={"configurable": {"session_id": session_id}},
    )


send_message(message="ei, como vai?", model_name="llama-3.1-8b-instant", session_id=78979)
# if __name__ == "main":
    