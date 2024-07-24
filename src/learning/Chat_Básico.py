from utils.model import model
import streamlit as st 
import textwrap

st.title('Chat Básico')
st.info('Esse chat não tem histórico.')

message = st.chat_input(placeholder='Sua Mensagem')

if message:
  res = model.invoke(message)

  
  
  st.text(textwrap.fill(res.content, width=80))

