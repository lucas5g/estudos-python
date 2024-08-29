import streamlit as st
from langchain_groq import ChatGroq

model = ChatGroq(temperature=0, model="llama3-8b-8192")

st.set_page_config(layout="wide")

st.title("Gerador de nomes para Empresa")
segment = st.text_input("Qual é o segmento da sua empresa?")

if segment:
    res = model.stream(
        f"Gera 5 ideias de nomes para empresas no segmento {segment}"
    )

    st.chat_message("assistant").write_stream(res)
