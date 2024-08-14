import streamlit as st
import datetime
import requests
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from typing import List
from enum import Enum


@tool
def date_today() -> str:
    """Retorna a data atual"""
    return datetime.date.today().strftime("%Y-%m-%d")


class ProvisionEnum(Enum):
    reuniao = "Reuniões Internas (presencial)"
    backend = "Análise de código fonte de aplicações Backend"
    testes = "Testes de qualidade do produto"


@tool
def productivity_create(provision: ProvisionEnum):
    """Criar produtividade passada como parametro e retorna sucesso ou falha no cadastro"""
    headers = {
        "Authorization": f"Bearer {st.session_state['jwt']}"

        # "Authorization": "Bearer eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlMTMyNTIwOC03ZmIzLTRhMWUtYjhhNC1mOGUyNWYzNTIxZWUiLCJ0eXBlIjoiVVNVQVJJT19JTlRFUk5PIiwiZmlzdCI6ZmFsc2UsImlhdCI6MTcyMzY1OTk1MywiZXhwIjoxNzIzNjY3MTUzLCJqdGkiOiIxMC4yMzAuMzIuMTIifQ.tOLRJSsKxcMrdCSHw8qV7uzwcxtCUmS-IOpa9OiDwGyNf83iItcw_7ejzf5TzH33"
    }

    payload = {
        "uuidMunicipio": "f1b365f5-e42f-4b03-ba5c-071b8e68b399",
        "nomeAreaSetor": "Superintendência de Tecnologia da Informação - STI",
        "nomePrestacao": provision.value,
        "atividadeFim": "Administrativa",
        "quantidadeServicoPrestado": "1",
        "sigla": "42",
        "atividade": "Ordinária",
        "dataLancamentoPrestacao": datetime.date.today().strftime("%Y-%m-%d")

    }

    res = requests.post(
        "https://dev.gerais.mg.def.br/sgp/service/lancar-prestacao",
        json=payload,
        headers=headers,
    )

    if res.status_code == 200:
        return f"{provision.value} foi cadastrada com sucesso :)"

    print(res.status_code, res.text, res.json)
    return f"{provision.value} falha no cadastro, tente mais uma vez"


@tool
def productivity_find() -> List:
    "Retorna as produtividades do usuário que solicitou"
    headers = {
        "Authorization": f"Bearer {st.session_state['jwt']}"
        # "Authorization": "Bearer eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlMTMyNTIwOC03ZmIzLTRhMWUtYjhhNC1mOGUyNWYzNTIxZWUiLCJ0eXBlIjoiVVNVQVJJT19JTlRFUk5PIiwiZmlzdCI6ZmFsc2UsImlhdCI6MTcyMzY1OTk1MywiZXhwIjoxNzIzNjY3MTUzLCJqdGkiOiIxMC4yMzAuMzIuMTIifQ.tOLRJSsKxcMrdCSHw8qV7uzwcxtCUmS-IOpa9OiDwGyNf83iItcw_7ejzf5TzH33"
    }

    res = requests.get(
        "https://dev.gerais.mg.def.br/sgp/service/lancar-prestacao/buscar-paginado/1-5",
        headers=headers,
    )

    productivities = [
        {
            "setor": productivity.get("nomeAreaSetor"),
            "serviço": productivity.get("nomePrestacao"),
            "data": productivity.get("dataLancamentoPrestacao"),
        }
        for productivity in res.json()["dados"]["dados"]
    ]

    return productivities


def get_response_model(query: str):
    model = ChatGroq(model="LLAMA-3.1-8B-INSTANT")

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Você é um assistente útil que retorna pedidos dos usuários"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    tools = [date_today, productivity_find, productivity_create]

    agent = create_tool_calling_agent(model, tools, prompt)

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor.invoke({"input": query})["output"]


def init():
    if "messages_agent" not in st.session_state:
        st.session_state["messages_agent"] = [
            {
                "role": "assistant",
                "content": "Olá! Sou o EstudoBot. O que você precisa de ajuda?",
            }
        ]


init()
title = "Agent"

st.set_page_config(page_icon="🤖", layout="wide", page_title=title)

st.header(title, divider=True, anchor=False)

# Lista todas as mensagens
for message in st.session_state["messages_agent"]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input("Mensagem Para o Agente")

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["messages_agent"].append({"role": "user", "content": prompt})

    res = get_response_model(prompt)

    st.chat_message("assistant").write(res)
    st.session_state["messages_agent"].append({"role": "assistant", "content": res})
