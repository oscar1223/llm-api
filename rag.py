from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI  # O HuggingFacePipeline
from dotenv import load_dotenv
import os

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

def get_qa_chain():
    vectorstore = Chroma(
        persist_directory="vectorstore",
        embedding_function=OpenAIEmbeddings()
    )
    retriever = vectorstore.as_retriever()
    llm = ChatOpenAI(openai_api_key=openai_key, model="gpt-3.5-turbo")

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
    return qa_chain
