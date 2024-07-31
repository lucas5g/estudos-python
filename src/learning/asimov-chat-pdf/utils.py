import streamlit as st 
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from pathlib import Path
from configs import *

PASTA_ARQUIVOS = Path(__file__).parent / "files"

def importacao_documentos():
    documentos = []
    for arquivo in PASTA_ARQUIVOS.glob("*.pdf"):
        loader = PyPDFLoader(str(arquivo))
        documentos_arquivo = loader.load()
        documentos.extend(documentos_arquivo)
    return documentos

def split_de_documentos(documentos):
    recur_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2500,
        chunk_overlap=250,
        separators=["/n\n", "\n", ".", " ", ""]
    )
    
    documentos = recur_splitter.split_documents(documentos)
    
    for i, doc in enumerate(documentos):
        doc.metadata["source"] = doc.metadata["source"].split("/")[-1]
        doc.metadata["doc_id"] = i
    
    return documentos

def cria_vector_store(documentos):
    embedding_model = OpenAIEmbeddings()
    
    vector_store = FAISS.from_documents(
        documents=documentos,
        embedding=embedding_model
    )
    
    return vector_store

def cria_chain_conversa():
    documentos = importacao_documentos()
    documentos = split_de_documentos(documentos)
    vector_store = cria_vector_store(documentos)
    
    chat = ChatOpenAI(model="gpt-3.5-turbo")
    memory = ConversationBufferMemory(
        return_messages=True,
        memory_key="chat_history", 
        output_key="answer"
    )
    
    retriever = vector_store.as_retriever(
        search_type=get_config("retrieval_search_type"),
        search_kwargs=get_config("retrieval_kwargs"),
        filter_fn=lambda x: x.metadata["source"] == "documentos.pdf"
    )
    
    prompt_template = PromptTemplate.from_template(get_config("retrieval_prompt_template"))
    chat_chain = ConversationalRetrievalChain.from_llm(
        llm=chat,
        memory=memory,
        retriever=retriever,
        return_source_documents=True,
        verbose=True,
        combine_docs_chain_kwargs={"prompt": prompt_template}
    )
    
    st.session_state["chain"] = chat_chain


