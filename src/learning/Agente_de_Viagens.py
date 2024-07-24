import streamlit as st
from utils.model import llm_groq as llm
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.utilities import SerpAPIWrapper
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables.base import RunnableSequence 
import os  

SerpAPIWrapper(serpapi_api_key=os.environ.get('SERPAPI_API_KEY'))
import bs4


def research_agent(query):
    tools = load_tools(["serpapi", "wikipedia"])
    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, prompt=prompt)

    res = agent_executor.invoke({"input": query})["output"]
    return res


def load_data():
    loader = WebBaseLoader(
        web_path="https://www.dicasdeviagem.com/inglaterra/",
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(class_=("postcontentwrap", "pagetitleloading"))
        ),
    )

    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    vector_store = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY")))

    return vector_store.as_retriever()


def get_relevant_docs(query):
    retriever = load_data()
    relevant_docs = retriever.get_relevant_documents(query)
    return relevant_docs


def supervisor_agent(query, web, relevant_documents):
    prompt_template = """
        Você é um gerente de uma agência de viagens. Sua resposta final deverá ser um roteiro de viagem completa e detalhada.
        Utilize o contexto de eventos e preços de passagens, o input do usuário e também os documentos relevantes 
        para elaborar o roteiro de viagens   
        Contexto: {web}
        Documento relevante: {relevant_documents}
        Usuário: {query},
        Assitente:
    """

    prompt = PromptTemplate(
        input_variables=["web", "relevant_documents","query"],
        template=prompt_template
    )

    sequence = RunnableSequence(prompt | llm)
    
    return sequence.invoke({ "web": web, "relevant_documents": relevant_documents, "query": query})

def get_response(query):
    web = research_agent(query)
    relevant_documents = get_relevant_docs(query)
    return supervisor_agent(query, web, relevant_documents)['content']


title = "Agente de Viagens"
# st.set_page_config(page_title=title, layout="wide")
st.title(title)
st.write("Eu posso te ajudar com algumas perguntas sobre a viagem:")

query = st.chat_input("Pergunte algo sobre a viagem para Inglaterra")
if query:
    st.chat_message("user").markdown(query)
    st.chat_message("assistant").write_stream(get_response(query))

