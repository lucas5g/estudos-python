import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from utils.model import model

st.title("Chat GPT-3.5-Turbo")

if "messagesGpt" not in st.session_state:
    st.session_state.messagesGpt = []

for message in st.session_state.messagesGpt:
    st.chat_message(message['role']).markdown(message["content"])

prompt = st.chat_input("Como posso ajudar?")
if prompt:
    st.chat_message("human").markdown(prompt)
    st.session_state.messagesGpt.append({"role": "human", "content": prompt})

    stream = model.stream(st.session_state.messagesGpt)
    res = st.chat_message("assistant").write_stream(stream)
    st.session_state.messagesGpt.append({"role":"assistant", "content": res})
