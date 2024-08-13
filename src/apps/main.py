import streamlit as st
import requests


def navigation():
    pg = st.navigation(
        [
            st.Page("chat.py", title="Meu Chat"),
            st.Page("assistente-youtube.py", title="Assistente Youtube"),
            st.Page("leitor-pdf.py", title="Leitor PDF"),
        ]
    )

    pg.run()


def main():
    st.set_page_config(layout="wide")

    with st.form("form_login"):
        token = st.text_input(
            "Token",
            placeholder="Token gerado no front. Ex: U2FsdGVkX19/4P3ffbr4TZEq...",
        )
        submit = st.form_submit_button("Login")

    if submit:
        payload = {"data": token}
        res = requests.post(
            "https://dev.gerais.mg.def.br/service/scsdp/login/interno", data=payload
        )

        st.session_state["jwt"] = res.text


if "jwt" not in st.session_state:
    st.session_state["jwt"] = ''
    main()
else:
    navigation()
