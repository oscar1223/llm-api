# 🚀 main.py

from fastapi import FastAPI  # Framework web para crear API
from pydantic import BaseModel  # Valida datos del request

from rag import get_qa_chain  # Cargamos la función que retorna la cadena RAG

app = FastAPI()
qa_chain = get_qa_chain()  # Inicializamos la cadena una vez

# Definimos el esquema de la petición
class Question(BaseModel):
    query: str

@app.post("/ask")
def ask_question(q: Question):
    response = qa_chain.invoke(q.query)
    for doc in response["source_documents"]:
        print("🧩", doc.page_content)

    print("Objeto", response)
    print("🔍 Respuesta: ", str(response["result"]))
    return {"answer": response}

conversations_by_user = {}

@app.post("/chat")
def chat_enpoint(q: Question):
    user_id = "racso"  # o pasar por header/body
    if user_id not in conversations_by_user:
        conversations_by_user[user_id] = ConversationChain(llm=llm, memory=ConversationBufferMemory())

    response = conversations_by_user[user_id].predict(input=q.query)
    return {"answer": response}