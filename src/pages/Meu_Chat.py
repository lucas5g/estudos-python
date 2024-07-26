import streamlit as st
import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def select_chat(chat_file):
    if not chat_file:
        st.session_state["messages"] = []
        return

    with open(f"src/chats/{chat_file}") as file:
        st.session_state["messages"] = json.load(file)
        st.session_state["chat_current"] = chat_file


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

title = "Meu Chat"
st.set_page_config(layout="wide", page_title=title)
model = st.selectbox(label="Modelos", options=["gpt-3.5-turbo", "gpt-4o-mini"])
st.title(f"{title} {model}")


if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_current" not in st.session_state:
    st.session_state["chat_current"] = ""

for message in st.session_state["messages"]:
    st.chat_message(message["role"]).markdown(message["content"])

prompt = st.chat_input("Mensagem Chat")
if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    stream = client.chat.completions.create(
        model=model,
        messages=st.session_state.messages,
        stream=True,
    )

    res = st.chat_message("ai").write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": res})

    chat_file = (
        f'{st.session_state["messages"][0]["content"][:35].replace(" ", "-")}.json'
    )
    st.session_state["chat_current"] = chat_file
    chat_path_file = f"src/chats/{chat_file}"
    with open(chat_path_file, "w", encoding="utf-8") as chat_file:
        json.dump(st.session_state["messages"], chat_file, indent=2, ensure_ascii=False)


tab1, tab2 = st.sidebar.tabs(["Mensagens", "Configurações"])

with tab1:

    st.button(
        "Nova Mensagem", use_container_width=True, on_click=select_chat, args=("",)
    )
    for chat in os.listdir("src/chats"):
        chat_name = chat.replace("-", " ").replace(".json", "").capitalize()

        st.button(
            chat_name,
            use_container_width=True,
            on_click=select_chat,
            args=(chat,),
            disabled=(chat == st.session_state["chat_current"]),
        )
