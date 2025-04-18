from fastapi import FastAPI
from pydantic import BaseModel
from rag import get_qa_chain

app = FastAPI()
qa_chain = get_qa_chain()

class Question(BaseModel):
    query: str

@app.post("/ask")
def ask_question(q: Question):
    result = qa_chain.run(q.query)
    return {"answer": result}
