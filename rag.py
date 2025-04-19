# 🤖 rag.py

from dotenv import load_dotenv
import os

from langchain_chroma import Chroma  # Recupera vectores desde el vectorstore persistente
from langchain_openai import OpenAIEmbeddings, ChatOpenAI  # Embeddings y LLM
from langchain.chains import RetrievalQA  # Chain para recuperar info y generar respuesta usando un LLM

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

def get_qa_chain():
    # Cargar la base de datos vectorial persistida
    vectorstore = Chroma(
        persist_directory="vectorstore",
        embedding_function=OpenAIEmbeddings(openai_api_key=openai_key)
    )
    retriever = vectorstore.as_retriever()

    # Modelo LLM
    llm = ChatOpenAI(openai_api_key=openai_key, model="gpt-4.1-nano")

    # Cadena RAG: consulta -> recupera chunks -> se los pasa al LLM
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True  # (opcional) para debug o trazabilidad
    )
    return qa_chain
