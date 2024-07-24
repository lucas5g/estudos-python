import streamlit as st
from utils.model import model
# from backend.generate_company_name import generate_company_name

st.set_page_config(layout='wide')

st.title("Gerador de nomes para Empresa")
segment = st.chat_input("Qual é o segmento da sua empresa?")

if segment:
  res = model.stream(f"Você é Gere 5 ideias de nomes para empresas no segmento {segment}")

  st.chat_message('assistant').write_stream(res)
