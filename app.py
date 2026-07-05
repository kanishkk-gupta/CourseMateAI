import os
import shutil
import streamlit as st

from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="RAG PDF Chat",
    page_icon="📚",
    layout="wide"
)

st.title("📚 RAG Chatbot")
st.write("Upload a PDF and chat with it.")

#########################################################
# API KEY
#########################################################

api_key = st.sidebar.text_input(
    "Mistral API Key",
    type="password"
)

if api_key:
    os.environ["MISTRAL_API_KEY"] = api_key

#########################################################
# Upload PDF
#########################################################

uploaded_pdf = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

#########################################################
# Create Database
#########################################################

if uploaded_pdf:

    save_path = os.path.join(
        "document loaders",
        uploaded_pdf.name
    )

    with open(save_path, "wb") as f:
        f.write(uploaded_pdf.getbuffer())

    st.success("PDF Uploaded Successfully")

    if st.button("Create Database"):

        with st.spinner("Creating Vector Database..."):

            #################################################
            # YOUR create_database.py CODE
            #################################################

            from langchain_community.document_loaders import PyPDFLoader
            from langchain_text_splitters import RecursiveCharacterTextSplitter
            from langchain_huggingface import HuggingFaceEmbeddings
            from langchain_community.vectorstores import Chroma

            loader = PyPDFLoader(save_path)
            docs = loader.load()

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )

            chunks = splitter.split_documents(docs)

            embedding_model = HuggingFaceEmbeddings(
                model_name="BAAI/bge-small-en-v1.5"
            )

            if os.path.exists("chroma_db"):
                shutil.rmtree("chroma_db")

            vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=embedding_model,
                persist_directory="chroma_db"
            )

            st.success("Database Created Successfully!")

#########################################################
# Chat Section
#########################################################

question = st.text_input("Ask your Question")

if st.button("Ask"):

    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_community.vectorstores import Chroma
    from langchain_mistralai import ChatMistralAI
    from langchain_core.prompts import ChatPromptTemplate

    embedding_model = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )

    vector_store = Chroma(
        persist_directory="chroma_db",
        embedding_function=embedding_model
    )

    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k":4,
            "fetch_k":10,
            "lambda_mult":0.5
        }
    )

    llm = ChatMistralAI(
        model="mistral-small-2506"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are a helpful AI assistant.

USE ONLY THE PROVIDED CONTEXT TO ANSWER THE QUESTION.

If the answer is not present in the context,
say:

"I couldn't find the answer in the document."
"""
            ),
            (
                "human",
                """
Context:
{context}

Question:
{Question}
"""
            )
        ]
    )

    docs = retriever.invoke(question)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    final_prompt = prompt.invoke(
        {
            "context": context,
            "Question": question
        }
    )

    response = llm.invoke(final_prompt)

    st.markdown("## Answer")

    st.write(response.content)

    with st.expander("Retrieved Chunks"):

        for i, doc in enumerate(docs):

            st.markdown(f"### Chunk {i+1}")

            st.write(doc.page_content)

            st.divider()