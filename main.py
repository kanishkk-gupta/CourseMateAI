from dotenv import load_dotenv
load_dotenv()

from langchain_huggingface import HuggingFaceEmbeddings
embedding_model= HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

from langchain_community.vectorstores import Chroma
vector_store = Chroma(persist_directory="chroma_db", embedding_function= embedding_model)
# Create a Retriever
retriever = vector_store.as_retriever(
    search_type="mmr", 
    search_kwargs={
        "k":4, 
        "fetch_k": 10, 
        "lambda_mult": 0.5})
 
from langchain_mistralai import ChatMistralAI
llm = ChatMistralAI(model= "mistral-small-2506")

from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """You are a helpful AI assistant. USE ONLY THE PROVIDED CONTEXT TO ANSWER THE QUESTION.
         If the answer is not present in the context, say: "I couldn't find the answer in the document."
         """),
        ("human", """Context : {context}
         Question: {Question}""")
    ]
)
print("RAG system Created")
print("Enter 0 to exit")

while True:
    querry = input("You: ")
    if querry== "0":
        break
    docs = retriever.invoke(querry)
    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    final_prompt= prompt.invoke({"context":context, "Question": querry})
    response = llm.invoke(final_prompt)
    print(f"\n AI: {response.content} ")
