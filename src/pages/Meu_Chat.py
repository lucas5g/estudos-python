import streamlit as st
from backend.model import find_model, models
from backend.database import Chat
st.set_page_config(page_title='Meu Chat', layout='wide')

#Header
model_name = st.selectbox(label='Modelos',options=models)
model = find_model(model_name)
print(model)

st.header(f"Meu Chat {model_name}")


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message['role']).markdown(message['content'])
    
prompt = st.chat_input("Mensagem Meu Chat")

if prompt:
    st.chat_message('user').markdown(prompt)
    st.session_state.messages.append({"role": "user", "content":prompt})
    
    stream = model.stream(st.session_state.messages)
    
    res = st.chat_message('assistant').write_stream(stream)
    st.session_state.messages.append({"role":"assistant", "content": res})

with st.sidebar:
    for chat in Chat.select():
        st.button(label=chat.name)
    
    
print(st.session_state.messages)