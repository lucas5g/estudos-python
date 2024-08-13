import streamlit as st
from langchain_groq import ChatGroq
from typing import List

def employee_find(name:str):
    if name == 'Lucas':
        return {name:'Lucas de Sousa Assunção', "position": "Backend"}
    return {"name": name, "position": "Frontend"}

def movies_current_find():
    
    return {"message":"list moviees"}

def events_weekend():
    from googlesearch.googlesearch import GoogleSearch
    response = GoogleSearch().search("eventos em bh")
    
    st.write(response)
    # for result in response.results:
    #     print("Title: " + result.title)
    #     print("Content: " + result.getText())
    
    
    
events_weekend()

def get_response_model(messages:List):
    model = ChatGroq(model="LLAMA-3.1-8B-INSTANT")   
    
    return model.stream(messages)



def init():

    if "messages_agent" not in st.session_state:
        st.session_state["messages_agent"] = []        

def main():
    title = "Agent"

    st.set_page_config(page_icon="🤖", layout="wide", page_title=title)

    st.header(title, divider=True, anchor=False)
    
    #Lista todas as mensagens
    for message in st.session_state["messages_agent"]:
        st.chat_message(message["role"]).write(message["content"])

    prompt = st.chat_input("Mensagem Para o Agente")

    if prompt:
        st.chat_message("user").write(prompt)
        st.session_state["messages_agent"].append({"role": "user", "content": prompt})

        stream = get_response_model(st.session_state['messages_agent'])

        res = st.chat_message("assistant").write_stream(stream)
        st.session_state["messages_agent"].append({"role": "assistant", "content": res})


init()
main()
