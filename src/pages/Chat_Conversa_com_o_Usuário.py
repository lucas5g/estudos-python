import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from utils.model import model

st.title("Chat conversa com o Usuário")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message.type).markdown(message.content)

prompt = st.chat_input("Como posso ajudar?")
if prompt:
    st.chat_message("human").markdown(prompt)
    st.session_state.messages.append(HumanMessage(content=prompt))

    stream = model.stream(st.session_state.messages)
    res = st.chat_message("assistant").write_stream(stream)
    st.session_state.messages.append(AIMessage(content=res))
