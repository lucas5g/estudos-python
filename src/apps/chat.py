import streamlit as st
from backend.model import find_model, models
from backend.database import Chat
from backend.chat import upsert_chat
import ast 

# st.set_page_config(layout="wide")

# Header
model_name = st.selectbox(label="Modelos", options=models)
model = find_model(model_name)

st.header(f"Meu Chat {model_name}")

if "chat_id" not in st.session_state:
    st.session_state.chat_id = False

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message["role"]).markdown(message["content"])

prompt = st.chat_input("Mensagem Meu Chat")

if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    stream = model.stream(st.session_state.messages)

    res = st.chat_message("assistant").write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": res})

    upsert_chat(st.session_state.chat_id, st.session_state.messages)


def select_chat(chat_id: int):
    st.session_state.chat_id = chat_id
    
    if not chat_id:
        st.session_state.messages = []
        return
    
    chat = Chat.get_by_id(chat_id)    
    st.session_state.messages = ast.literal_eval(chat.history)


with st.sidebar:
    st.button(
        label="Nova Mensagem", use_container_width=True, on_click=select_chat, args=(0,)
    )
    for chat in Chat.select():
        st.button(
            label=chat.name,
            key=chat.id,
            use_container_width=True,
            on_click=select_chat,
            args=(chat.id,),
            disabled=(chat.id == st.session_state.chat_id)
        )
