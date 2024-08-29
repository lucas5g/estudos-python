from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import os
import streamlit as st


def loader(file: str):
    with open("temp.pdf", "wb") as f:
        f.write(file.getbuffer())
    loader = PyPDFLoader("temp.pdf")
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    documents_splits = text_splitter.split_documents(documents)
    db = FAISS.from_documents(documents_splits, embedding=OpenAIEmbeddings())
    
    return db 

def find_similarity(db:FAISS, query:str):
    documents_similarity = db.similarity_search(query)
    page_contents = [doc.page_content.replace("\n", "") for doc in documents_similarity]
    return "".join(page_contents)
    
def handle_prompt(contents: str, query:str):
    
    prompt = f"""
        Você é um assistente que todo seu conhecimento está no texto abaixo.
        "{contents}",
        Caso tenho algo fora do conteúdo, responda "No momento ainda não tenho essa informação".
        Não retorne na sua resposta "De acordo com o conteúdo fornecido"
        Responda: {query}.
    """ 

    model = ChatGroq(
        temperature=0, model="llama3-70b-8192", api_key=os.getenv("GROQ_API_KEY")
    )

    return model.stream(prompt)   
    
def main(file: str, query: str):    
    db = loader(file)
    contents = find_similarity(db, query)
    
    return handle_prompt(contents, query)
 
title = "Leitor PDF"

st.title(title)

file = st.file_uploader("Escolha um PDF e faça pesquisas no documento", "pdf")
query = st.chat_input("Busque no PDF.")


if file and query:
    st.chat_message("user").markdown(query)
    res = main(file, query)
    st.chat_message("ai").write_stream(res)
