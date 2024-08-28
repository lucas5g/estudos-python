import streamlit as st
from backend.meu_chat import models, find_model, history, with_message_history, send_message
from langchain_core.messages import HumanMessage, AIMessage

#init 
def init():    
    st.set_page_config(
        page_title="Meu Chat", page_icon=":left_speech_bubble:", layout="wide"
    )
    if "session_id" not in st.session_state:
        st.session_state.session_id = False

    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    if "model" not in st.session_state:
        st.session_state["model"] = ""

def main():
    # Header
    model_name = st.selectbox(label="Modelos", options=models)
    print(model_name)    

init()
main()



# st.session_state["model"] = find_model(model_name)
# model = find_model(model_name)

# st.markdown(
#     f"""
#     ## Meu Chat {model_name}
#     """
# )
# for message in history.messages:
#     if isinstance(message, HumanMessage):
#         st.chat_message("user").markdown(message.content)
#     elif isinstance(message, AIMessage):
#         st.chat_message("assistant").markdown(message.content)

# prompt = st.chat_input("Mensagem Meu Chat")

# if prompt:
#     stream = send_message(prompt)
#     st.chat_message("assistant").write_stream(stream)
    
#     st.chat_message("user").markdown(prompt)
#     st.session_state.messages.append({"role": "user", "content": prompt})
    
#     st.session_state.messages.append({"role": "assistant", "content": res})

#     upsert_chat(st.session_state.chat_id, st.session_state.messages)


# def select_chat(chat_id: int):
#     st.session_state.chat_id = chat_id

#     if not chat_id:
#         st.session_state.messages = []
#         return

#     chat = Chat.get_by_id(chat_id)
#     st.session_state.messages = ast.literal_eval(chat.history)


# with st.sidebar:
#     st.button(
#         label="Nova Mensagem", use_container_width=True, on_click=select_chat, args=(0,)
#     )
#     for chat in Chat.select():
#         st.button(
#             label=chat.name,
#             key=chat.id,
#             use_container_width=True,
#             on_click=select_chat,
#             args=(chat.id,),
#             disabled=(chat.id == st.session_state.chat_id)
#         )
