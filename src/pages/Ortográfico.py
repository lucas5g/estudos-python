import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

st.set_page_config(page_title="Ortográfico", layout="wide")

st.header("Ortográfico")

text = st.text_area(
    label="Texto que deseja verificar a ortográfia",
    placeholder="Insira o texto aqui",
    height=100,
)

if text:

    prompt_template = ChatPromptTemplate.from_messages(
        [("system", "Corrija a ortografia do texto e retorne somente o resultado da correção."), ("user", "{text}")]
    )

    model = ChatGroq(temperature=0, model="llama3-8b-8192")

    chain = prompt_template | model | StrOutputParser()

    res = chain.invoke(text)

    st.text("Correção:")
    st.code(res)

