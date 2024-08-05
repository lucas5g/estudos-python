import streamlit as st
from datetime import datetime
from backend.database import Chat


def upsert_chat(chat_id, messages):
    if chat_id:
        return Chat.update(history=messages, updated_at=datetime.now()).where(
            Chat.id == chat_id
        )

    chat = Chat(
        name=messages[0]["content"][:30],
        history=messages,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    chat.save()
    st.session_state.chat_id = chat.id
    return chat.id
