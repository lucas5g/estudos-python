import os
from dotenv import load_dotenv
import streamlit as st
from transformers import AutoTokenizer
import requests

load_dotenv()

modelos = {
    "mistralai/Mixtral-8x7B-Instruct-v0.1": "[/INST]",
    "google/gemma-7b-it": "<start_of_turn>model\n",
}


modelo = st.selectbox("Selecion um modelo: ", options=modelos)
token_modelo = modelos[modelo]


if "modelo_atual" not in st.session_state or st.session_state["modelo_atual"] != modelo:
    st.session_state["modelo_atual"] = modelo
    st.session_state["mensagens"] = []

nome_modelo = st.session_state["modelo_atual"]
tokenizer = AutoTokenizer.from_pretrained(nome_modelo, token=os.getenv("HF_KEY"))
url = f"https://api-inference.huggingface.co/models/{nome_modelo}"
headers = {"Authorization": f"Bearer {os.getenv('HF_KEY')}"}

mensagens = st.session_state["mensagens"]
area_chat = st.empty()

pergunta_usuario = st.chat_input("Faça a sua pergunta aqui:")

if pergunta_usuario:
    mensagens.append({"role": "user", "content": pergunta_usuario})
    template = tokenizer.apply_chat_template(
        mensagens, tokenize=False, add_generation_prompt=True
    )
    json = {
        "inputs": template,
        "parameters": {"max_new_tokens": 1000},
        "options": {"use_cache": False, "wait_for_model": True},
    }

    res = requests.post(url, json=json, headers=headers).json()
    mensagem_chat = res[0]["generated_text"].split(token_modelo)[-1]
    mensagens.append({"role": "assistant", "content": mensagem_chat})

with area_chat.container():
    for mensagem in mensagens:
        chat = st.chat_message(mensagem["role"])
        chat.markdown(mensagem["content"])
