import streamlit as st
import time
import asyncio
from backend.meu_chat import send_message, get_session_history
from langchain_core.messages import HumanMessage, AIMessage


st.set_page_config(
    page_title="Meu Chat", page_icon=":left_speech_bubble:", layout="wide"
)


if "session_id" not in st.session_state:
    st.session_state["session_id"] = int(time.time())

model_name = st.selectbox(
    "Modelos",
    [
        "LLAMA-3.1-8B-INSTANT",
        "LLAMA3-8B-8192",
        "GPT-3.5-TURBO",
        "GPT-4o",
    ],
)

st.markdown(
    f"""
    ## Meu Chat {model_name}
    
    """
)


for message in get_session_history(st.session_state["session_id"]).messages:
    if isinstance(message, HumanMessage):
        st.chat_message("user").markdown(message.content)
    elif isinstance(message, AIMessage):
        st.chat_message("assistant").markdown(message.content)


prompt = st.chat_input("Mensagem Meu Chat")

if prompt:
    st.chat_message("user").markdown(prompt)

    stream = send_message(
        message=prompt,
        model_name=model_name,
        session_id=st.session_state["session_id"],
    )

    st.chat_message("assistant").write_stream(stream)


# # def select_chat(chat_id: int):
# #     st.session_state.chat_id = chat_id

# #     if not chat_id:
# #         st.session_state.messages = []
# #         return

# #     chat = Chat.get_by_id(chat_id)
# #     st.session_state.messages = ast.literal_eval(chat.history)


# with st.sidebar:
#     st.button("Nova Mensagem", use_container_width=True)

#     db = SqliteDatabase("memory.db")

#     class Message(Model):
#         session_id = IntegerField()
#         message = CharField()

#         class Meta:
#             database = db
#             table_name = "message_store"

#     db.connect()

#     messages = Message.select(Message.session_id, Message.message).distinct()

#     for message in messages:
#         st.write(message.message)
#         # st.button(label=str(message.message), use_container_width=True)
