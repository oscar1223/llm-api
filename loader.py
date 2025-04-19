# 📄 loader.py

from dotenv import load_dotenv  # Carga variables desde .env
import os

from langchain.text_splitter import RecursiveCharacterTextSplitter  # Divide textos en fragmentos manejables
from langchain_community.document_loaders import TextLoader  # Carga documentos desde archivos de texto plano
from langchain_openai import OpenAIEmbeddings  # Crea vectores a partir de texto usando OpenAI
from langchain_chroma import Chroma  # Vectorstore para almacenar y consultar los vectores embebidos

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

def load_and_index_docs():
    loader = TextLoader("faq.txt")  # Carga el documento con las preguntas/respuestas
    docs = loader.load()

    # Divide el texto en bloques más pequeños con solapamiento
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs_split = splitter.split_documents(docs)

    # Crea una base de datos vectorial persistente
    vectorstore = Chroma.from_documents(
        documents=docs_split,
        embedding=OpenAIEmbeddings(openai_api_key=openai_key),
        persist_directory="vectorstore"
    )
    print("📦 Vectorstore creado y persistido exitosamente.")

if __name__ == "__main__":
    load_and_index_docs()
