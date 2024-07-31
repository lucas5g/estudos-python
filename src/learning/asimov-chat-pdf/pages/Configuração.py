import json 
import streamlit as st 
from configs import get_config
from utils import PASTA_ARQUIVOS, cria_chain_conversa
st.header("Página de configuração", divider=True)

model_name = st.text_input("Modifique o modelo", value=get_config("model_name"))
retrieval_search_type = st.text_input("Modifique o tipo de retrieval", value=get_config("retrieval_search_type"))
retrieval_kwargs = st.text_input("Modifique os parâmetros de retrieval", value=json.dumps(get_config("retrieval_kwargs")))
prompt = st.text_area("Modifique o prompt padrão", height=350, value=get_config("prompt"))


if st.button("Modifique parâmetros", use_container_width=True):
    st.session_state["model_name"] = model_name
    st.session_state["retrieval_search_type"] = retrieval_search_type
    st.session_state["retrieval_kwargs"] = json.loads(retrieval_kwargs)
    st.session_state["prompt"] = prompt
    
if st.button("Atualiza ChatBot", use_container_width=True):
    if len(list(PASTA_ARQUIVOS.glob("*.pdf"))) == 0:
        st.error("Você não adicionou nenhum arquivo PDF.")
    else:
        st.success("Inicializando o ChatBot...")
        cria_chain_conversa()
        st.rerun()