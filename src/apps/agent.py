import streamlit as st
import datetime
import requests
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from typing import List


@tool
def date_today() -> str:
    """Retorna a data atual"""
    return datetime.date.today().strftime("%Y-%m-%d")


@tool
def productivity_find() -> List:
    "Retorna uma lista de dicionários de produtividade"
    res = requests.get(
        "https://dev.gerais.mg.def.br/sgp/service/lancar-prestacao/buscar-paginado/1-5",
        headers={"Authorization": f"Bearer {st.session_state['jwt']}"},
    )

    productivities = [
        {
            "nomeAreaSetor": productivity.get("nomeAreaSetor"),
            "nomePrestacao": productivity.get("nomePrestacao"),
        }
        for productivity in res.json()["dados"]["dados"]
    ]

    return productivities

# @tool 



def get_response_model(query: str):
    model = ChatGroq(model="LLAMA-3.1-8B-INSTANT")

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Você é um assistente útil"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    tools = [date_today, productivity_find]

    agent = create_tool_calling_agent(model, tools, prompt)

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor.invoke({"input": query})["output"]


def init():
    if "messages_agent" not in st.session_state:
        st.session_state["messages_agent"] = []


def main():
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
        # res = get_response_model(st.session_state["messages_agent"])
        # res = get_response_model(st)

        st.chat_message("assistant").write(res)
        st.session_state["messages_agent"].append({"role": "assistant", "content": res})


init()
main()
