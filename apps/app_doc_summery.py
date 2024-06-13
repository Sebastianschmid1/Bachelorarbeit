import time
import streamlit as st
import streamlit.components.v1 as components

from langchain.chains import MapReduceDocumentsChain, ReduceDocumentsChain
from langchain_text_splitters import CharacterTextSplitter

from langchain.chains import AnalyzeDocumentChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain_openai import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.chains.llm import LLMChain
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate

from PyPDF2 import PdfReader, PdfWriter

import os

from dotenv import load_dotenv


load_dotenv(".env")
docs = []
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
    model="gpt-4-turbo",
    temperature=0,
)
user_input = "Write a concise summary of the following:"
pdf_dict_path = "pdfs"


def prompt_costume_template(user_input: str) -> PromptTemplate:
    prompt_template = """:
    "{text}"
    CONCISE SUMMARY:"""

    return PromptTemplate.from_template(user_input + prompt_template)


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


def load_pdf_files(folder_path):
    """Lade alle PDF-Dateinamen in einem Ordner."""
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(".pdf"):
            st.sidebar.write(file_name)
            (
                docs
                + PyPDFLoader(f"{folder_path}/{file_name}", extract_images=False).load()
            )
            print(type(docs))


def get_openai_response(question: str) -> str:
    if docs is not None:
        t1 = time.time()
        print("starting")
        prompt = prompt_costume_template(question)
        reduce_chain = LLMChain(llm=chat, prompt=prompt)
        combine_documents_chain = StuffDocumentsChain(
            llm_chain=reduce_chain, document_variable_name="text"
        )
        print("progress:  combine_documents_chain" + str(time.time() - t1))
        reduce_documents_chain = ReduceDocumentsChain(
            combine_documents_chain=combine_documents_chain,
            collapse_documents_chain=combine_documents_chain,
            token_max=8000,
        )
        print("progress:  reduce_documents_chain" + str(time.time() - t1))
        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=4000, chunk_overlap=3
        )
        print("progress:  CharacterTextSplitter" + str(time.time() - t1))
        split_docs = text_splitter.split_documents(docs)
        print("progress:  split_docs" + str(time.time() - t1))
        return reduce_documents_chain.run(split_docs)
    else:
        return "Bitte laden Sie zuerst eine Datei hoch"


st.set_page_config(
    page_title="BA",
    page_icon="👾",
)
st.header("Bachelorsarbeit Application")
st.sidebar.title("Upload-Button Beispiel")
load_pdf_files(pdf_dict_path)
uploaded_file = st.sidebar.file_uploader("Datei hier hochladen:", type=["pdf", "csv"])
k = 0
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
