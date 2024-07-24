import streamlit as st
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from utils.model import model

import os

load_dotenv()

embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))


def create_vector_from_youtube_url(video_url: str) -> FAISS:
    loader = YoutubeLoader.from_youtube_url(video_url, language="pt")

    # aqui ta o texto do vídeo
    trasncript = loader.load()

    text_spliter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_spliter.split_documents(trasncript)

    db = FAISS.from_documents(docs, embeddings)

    return db


# O k representa quantos retornos do banco
def get_response_from_query(db, query, k=4):
    docs = db.similarity_search(query, k)
    docs_page_content = " ".join([d.page_content for d in docs])

    chat_template = ChatPromptTemplate.from_messages(
        [
            (
                "user",
                """Você é um assitente que responde perguntas sobre vídeos do youtube baseado na transcrição do vídeo
                Responda a seguinte pergunta: {pergunta}
                Procurando nas seguintes transcrições: {docs}
                Use somente informações da transcrição para responder a pergunta. Caso você não encontre nada, responda com "Eu não sei"
                Suas respostas devem ser detalhadas 
				""",
            )
        ]
    )

    chain = chat_template | model

    res = chain.stream({"pergunta": query, "docs": docs_page_content})

    return res, docs


st.title("Assitente do YouTube!")

youtube_url = st.text_input(
    label="URL do YouTube", placeholder="Cole o link do YouTube aqui."
)
query = st.text_input(
    label="Pergunta Sobre algo do vídeo!", placeholder="Ex: Sobre o que fala o vídeo.."
)
button = st.button(label="Perguntar")

if youtube_url and query and button:
    db = create_vector_from_youtube_url(youtube_url)
    res, docs = get_response_from_query(db, query)

    st.chat_message('assistant').write_stream(res)
