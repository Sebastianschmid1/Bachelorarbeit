from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

import streamlit as st
import streamlit.components.v1 as components
import os

load_dotenv(".env")
response: str = ""
chat = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.6,
)

models = [
    "gpt-4o",
    "gpt-3.5-turbo",
    "gpt-4",
    "gpt-4-turbo",
    "gpt-4-vision-preview",
    "davinci-002",
    "babbage-002",
]


def alert(message: str) -> None:
    components.html(
        f"""
        <script>
        alert({message});
        </script>
        """,
        height=0,
        width=0,
    )


def get_openai_response(question: str, sytem_message: str) -> str:
    if type(question) == str and type(sytem_message) == str:
        messages = [
            SystemMessage(content=sytem_message),
            HumanMessage(content=question),
        ]

        return chat(messages).content
    else:
        return "Bitte laden Sie zuerst eine Datei hoch"


st.set_page_config(
    page_title="BA",
    page_icon="👾",
)
st.header("Bachelorarbeit Application")

model_choice = st.selectbox("Choose a chat model:", models)
chat.model_name = model_choice
st.write(f"You selected: {chat.model_name}")


sytem_message = st.text_input(
    "InputSystem: ",
    key="inputSystem",
    value="Du bist ein hilfreicher Assistent für Fragen im Bereich Erdkunde?",
)
input_user = st.text_area("InputUser: ", key="input", height=150)
submit = st.button("Ask the question")

if submit:
    response = get_openai_response(input_user, sytem_message)
if submit and (response != ""):
    st.subheader("The Response is")
    st.write(response)
