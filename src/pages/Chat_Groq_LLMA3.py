from langchain_core.messages import AIMessage, HumanMessage
from utils.model import llm_groq as model
import streamlit as st
import json
st.title("Chat Groq LLMA3")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message['role']).markdown(message["content"])

message = st.chat_input("Mensagem para o Groq/llama3")
if message:

    st.chat_message("human").markdown(message)
    st.session_state.messages.append({"role": "human", "content": message})

    stream = model.stream(st.session_state.messages)
    res = st.chat_message("assistant").write_stream(stream)
    st.session_state.messages.append({"role":"assistant", "content": res})
