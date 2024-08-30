import streamlit as st
from langchain_groq import ChatGroq

chat = ChatGroq(model="llama-3.1-8b-instant")

#init
if "messages" not in st.session_state:
    st.session_state["messages"] = []


##main

st.header("Chat Llama3.1 Groq")

for message in st.session_state["messages"]:
    st.chat_message(message["role"]).markdown(message["content"])


promtp = st.chat_input("Mande sua dúvida")

if promtp:
    st.chat_message('user').markdown(promtp)
    st.session_state["messages"].append({"role": "user", "content": promtp})
    
    stream = chat.stream(st.session_state["messages"])
    
    res = st.chat_message("assistant").write_stream(stream)    
    st.session_state["messages"].append({"role": "assistant", "content": res})
    
def clear_messages():
    st.session_state["messages"] = []
with st.sidebar:
    st.button("Limpar Histórico", use_container_width=True, on_click=clear_messages)