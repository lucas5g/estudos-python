from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType
import pandas as pd
import streamlit as st
from utils.model import llm_groq as llm
# from utils.model import model as llm

sheet = "https://docs.google.com/spreadsheets/d/11DFicldhwNKykwCWbn_j9NwPDgKJ7fj9vNc5MqLqJRI/export?gid=0&format=csv"
df = pd.read_csv(sheet)

prefix = """"
    Você se chama Ana, e está trabalhando com dataframe pandas no Python. 
    O nome do Datafra é `df`
    Responda sempre em Português.
    E retorne somente o texto
"""

agent = create_pandas_dataframe_agent(
    llm=llm,
    df=df,
    prefix=prefix,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
    allow_dangerous_code=True,
)

st.title('Análise dos Dados')
prompt = st.chat_input("Análise de dados sobre o Brasil.")
if prompt:
    st.chat_message("user").markdown(prompt)
    res = agent.invoke(prompt) 
    st.chat_message("assistant").markdown(res['output'])
