from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain.cache import InMemoryCache
from langchain.chains import AnalyzeDocumentChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain_openai import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.chains.llm import LLMChain
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import CharacterTextSplitter
from langchain.chains import ReduceDocumentsChain
import streamlit as st

import streamlit.components.v1 as components

from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


from dotenv import load_dotenv

load_dotenv(".env")
uploaded_file = None
faiss_index: FAISS = None
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
response = ""
models = [
    "gpt-4o",
    "gpt-4-turbo",
    "gpt-3.5-turbo",
    "gpt-4",
    "gpt-4-vision-preview",
    "davinci-002",
    "babbage-002",
]

chat = ChatOpenAI(model="gpt-4o", temperature=0.6, cache=InMemoryCache())


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

        doc_in_text = ""
        for i in doc:
            doc_in_text += i.page_content
        print("_________________________________________________________")
        print(doc_in_text)
        messages = [
            SystemMessage(
                content="Sei ein hilfreicher VDA 4938 Assistent mit folgendem Kontext:"
                + doc_in_text
            ),
            HumanMessage(content=question),
        ]
        return chat(messages).content
    else:
        return "Bitte laden Sie zuerst eine Datei hoch"


def get_openai_response_extansion(question: str) -> str:
    if uploaded_file:
        prompt_template = """:
        "{text}"
        CONCISE SUMMARY:"""
        reduce_chain = LLMChain(
            llm=chat, prompt=PromptTemplate.from_template(question + prompt_template)
        )
        combine_documents_chain = StuffDocumentsChain(
            llm_chain=reduce_chain, document_variable_name="text"
        )
        reduce_documents_chain = ReduceDocumentsChain(
            combine_documents_chain=combine_documents_chain,
            collapse_documents_chain=combine_documents_chain,
            token_max=8000,
        )
        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=4000, chunk_overlap=3
        )
        temp_file = "./temp.pdf"

        with open(temp_file, "wb") as file:
            file.write(uploaded_file.getvalue())

        split_docs = text_splitter.split_documents(
            PyPDFLoader(
                temp_file,
                extract_images=False,
            ).load()
        )
        return reduce_documents_chain.run(split_docs)
    else:
        return "Bitte laden Sie zuerst eine Datei hoch"


def laod_pdf() -> FAISS:
    temp_file = "./temp.pdf"

    with open(temp_file, "wb") as file:
        file.write(uploaded_file.getvalue())

    loader = PyPDFLoader(temp_file)
    pages = loader.load_and_split()
    faiss_index = FAISS.from_documents(pages, embeddings)
    return faiss_index


if __name__ == "__main__":
    st.set_page_config(
        page_title="BA",
        page_icon="👾",
    )
    st.header("Bachelorsarbeit Application")
    st.sidebar.title("Upload-Button Beispiel")
    uploaded_file = st.sidebar.file_uploader(
        "Datei hier hochladen:", type=["pdf", "csv"]
    )
    model_choice = st.selectbox("Choose a chat model:", models)
    chat.model_name = model_choice
    st.write(f"You selected: {chat.model_name}")
    input_user = st.text_area("InputUser: ", key="input", height=150)
    submit = st.button("Ask the question")

    if uploaded_file:

        if uploaded_file.type == "text/csv":
            st.write("PDF-Datei wurde hochgeladen.")
        elif uploaded_file.type == "application/pdf":
            faiss_index = laod_pdf()
            st.write("PDF-Datei wurde hochgeladen.")
            alert("Datei erfolgreich hochgeladen!")

    else:
        st.warning("Bitte eine Datei hochladen.")

    if submit:
        response = get_openai_response(input_user)
    if submit and (response != ""):
        st.subheader("The Response is")
        st.write(response)

    sum_up = st.button("Summary")
    if sum_up:
        response = get_openai_response_extansion(input_user)
    if sum_up and (response != ""):
        st.subheader("The Response is")
        st.write(response)
