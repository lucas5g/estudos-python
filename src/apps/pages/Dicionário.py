import streamlit as st
import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

system_template = """
Retorne uma lista 
    com o significado ou tradução em português das seguintes palavras
    ###
    {words}
    ###
    
    Retorne igual o examplo abaixo
    Equidade: Característica de algo ou alguém que revela senso de justiça, que julga de maneira imparcial, isenta e neutra, sem tomar partidos; imparcialidade: duvidou da equidade das eleições.
    
 """

prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{words}")]
)

model = ChatGroq(api_key=os.getenv("GROQ_API_KEY"))

parser = StrOutputParser()

chain = prompt_template | model | parser

st.set_page_config(layout="wide")
st.title("Dicionário")

words = st.text_area(label="Palavras", placeholder="Passe uma lista de Palavras.")
if words:
    stream = chain.stream({"words": words})
    st.write_stream(stream)


[
    {"role": "user", "content": "1+1"},
    {"role": "assistant", "content": "1 + 1 = 2"},
    {"role": "user", "content": "2+2"},
    {"role": "assistant", "content": "2 + 2 = 4"},
]
