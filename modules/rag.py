# rag_chat.py
from dotenv import load_dotenv
import os
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from .mongo_memory import MongoMemory

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

# Recuperador
retriever = Chroma(
    persist_directory="vectorstore",
    embedding_function=OpenAIEmbeddings(openai_api_key=openai_key)
).as_retriever()

# Diccionario de sesiones
user_sessions = {}

def get_chain_for_user(user_id: str):
    if user_id not in user_sessions:
        memory = MongoMemory(user_id=user_id)
        chain = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(openai_api_key=openai_key, model="gpt-4.1-nano"),
            retriever=retriever,
            memory=memory,
            verbose=False
        )
        user_sessions[user_id] = chain
    return user_sessions[user_id]
