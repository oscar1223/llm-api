from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings  # O HuggingFaceEmbeddings

def load_and_index_docs():
    loader = TextLoader("faq.txt")
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs_split = splitter.split_documents(docs)

    vectorstore = Chroma.from_documents(
        documents=docs_split,
        embedding=OpenAIEmbeddings(),  # Usa tus credenciales
        persist_directory="vectorstore"
    )
    vectorstore.persist()
    return vectorstore
