# 🚀 main.py
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException, Header  # Framework web para crear API
from pydantic import BaseModel  # Valida datos del request
from modules.rag import get_chain_for_user  # Cargamos la función que retorna la cadena RAG
from modules.auth import register_user, login_user
from modules.jwt_utils import verify_token  # Verifica el token JWT

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_user_id_from_token(authorization: str = Header(...)):
    token = authorization.split("Bearer ")[-1]
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido")
    return payload["user_id"]

# 🔐 Autenticación
class AuthRequest(BaseModel):
    username: str
    password: str

@app.post("/register")
def register(data: AuthRequest):
    return register_user(data.username, data.password)

@app.post("/login")
def login(data: AuthRequest):
    return login_user(data.username, data.password)


# 💬 Chat con memoria + RAG
class ChatRequest(BaseModel):
    user_id: str
    query: str

conversations_by_user = {}

@app.post("/chat")
def chat(req: ChatRequest, user_id: str = Depends(get_user_id_from_token)):
    chain = get_chain_for_user(req.user_id)
    result = chain.invoke({"question": req.query})
    return {
        "👀 answer": result["answer"],
        "🗒️ sources": [doc.page_content for doc in result.get("source_documents", [])]
    }