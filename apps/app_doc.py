from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
import streamlit as st

import streamlit.components.v1 as components

from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from PyPDF2 import PdfReader, PdfWriter

import os

from dotenv import load_dotenv

load_dotenv(".env")

faiss_index: FAISS = None
embeddings = OpenAIEmbeddings()
response = ""
models = [
    "gpt-3.5-turbo",
    "gpt-4",
    "gpt-4-turbo",
    "gpt-4-vision-preview",
    "davinci-002",
    "babbage-002",
]
chat = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.6,
)


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


def get_openai_response(question: str) -> str:
    if faiss_index is not None:

        doc = faiss_index.similarity_search(question, k=2)
        print(doc[0].page_content)
        messages = [
            SystemMessage(content=question +" mit Folgenden Kontext:"),
            HumanMessage(content=doc[0].page_content),
        ]
        return chat(messages).content
    else:
        return "Bitte laden Sie zuerst eine Datei hoch"


st.set_page_config(
    page_title="BA",
    page_icon="👾",
)
st.header("Bachelorsarbeit Application")

st.sidebar.title("Upload-Button Beispiel")
uploaded_file = st.sidebar.file_uploader("Datei hier hochladen:", type=["pdf", "csv"])

if uploaded_file is not None:

    if uploaded_file.type == "text/csv":
        st.write("PDF-Datei wurde hochgeladen.")
    elif uploaded_file.type == "application/pdf":

        pdf_reader = PdfReader(uploaded_file)
        pdf_writer = PdfWriter()

        # Kopieren der Seiten vom PdfReader zum PdfWriter
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

        with open(f"pdfs/{uploaded_file.name}", "wb") as output_pdf_file:
            pdf_writer.write(output_pdf_file)

        loader = PyPDFLoader(f"pdfs/{uploaded_file.name}", extract_images=False)
        pages = loader.load_and_split()
        faiss_index = FAISS.from_documents(pages, embeddings)

        st.write("PDF-Datei wurde hochgeladen.")

        alert("Datei erfolgreich hochgeladen!")

else:
    st.warning("Bitte eine Datei hochladen.")

model_choice = st.selectbox("Choose a chat model:", models)
chat.model_name = model_choice
st.write(f"You selected: {chat.model_name}")
input_user = st.text_area("InputUser: ", key="input", height=150)
submit = st.button("Ask the question")
if submit:
    response = get_openai_response(input_user)
if submit and (response != ""):
    st.subheader("The Response is")
    st.write(response)
