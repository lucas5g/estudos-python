import streamlit as st
from langchain.memory import ConversationBufferMemory
from utils import PASTA_ARQUIVOS, cria_chain_conversa
    
def sidebar():
    uploaded_pdfs = st.file_uploader(
        "Adicione seus arquivos pdf",
        type=[".pdf"],
        accept_multiple_files=True
    )
    
    if not uploaded_pdfs is None:
        for arquivo in PASTA_ARQUIVOS.glob(".pdf"):
            arquivo.unlink()
        for pdf in uploaded_pdfs:
            with open(PASTA_ARQUIVOS / pdf.name, 'wb') as f:
                f.write(pdf.read())
                
    label_botao = "Inicializar ChatBot"
    
    if "chain" in st.session_state:
        label_botao = "Atualizar ChatBot"
        
    if st.button(label_botao, use_container_width=True):
        if len(list(PASTA_ARQUIVOS.glob("*.pdf"))) == 0:
            st.error("Você não adicionou nenhum arquivo PDF.")
        else:
            st.success("Inicializando o ChatBot...")
            cria_chain_conversa()
            st.rerun()

def chat_window():
    st.header("Bem-vindo ao Chat com PDFS da Asimov", divider=True)
    
    if not "chain" in st.session_state:
        st.error("Faça o upload de PDFs para começar!")
        st.stop()

    chain = st.session_state["chain"]        
    memory = chain.memory
    
    mensagens = memory.load_memory_variables({})["chat_history"]  
    
    container = st.container()    
    for mensagem in mensagens:
        chat = container.chat_message(mensagem.type)
        chat.markdown(mensagem.content)
        
    nova_mensagem = st.chat_input("Converse com seus documentos...")
    if nova_mensagem:
        chat = container.chat_message("human")
        chat.markdown(nova_mensagem)       
        chat = container.chat_message("ai")
        chat.markdown("Gerando resposta...")
        
        chain.invoke({"question": nova_mensagem})
        st.rerun()


def main():
    with st.sidebar:
        sidebar()
    chat_window()
    
main()