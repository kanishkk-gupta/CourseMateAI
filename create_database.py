#This file is Only responsible for creating the database. Run only once (or whenever documents change). So we didn't wrote this in main.py because creating the vector database is a one-time (or occasional) task, while main.py runs every time the user asks a question.
# LOAD PDF
# SPLIT INTO CHUNKS
# CREATE THE EMBEDDINGS
# STORE INTO CHROMADB

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from dotenv import load_dotenv
load_dotenv()

loader = PyPDFLoader("document loaders/deeplearning.pdf")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
chunks = splitter.split_documents(docs)

embedding_model = HuggingFaceEmbeddings(model_name= "BAAI/bge-small-en-v1.5")

vectorstore = Chroma.from_documents(documents = chunks, embedding=embedding_model , persist_directory="chroma_db")

