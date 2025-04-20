# loader.py
from dotenv import load_dotenv
import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

def load_and_index_docs():
    loader = TextLoader("faq.txt")
    docs = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs_split = splitter.split_documents(docs)

    Chroma.from_documents(
        documents=docs_split,
        embedding=OpenAIEmbeddings(openai_api_key=openai_key),
        persist_directory="vectorstore"
    )

if __name__ == "__main__":
    load_and_index_docs()
