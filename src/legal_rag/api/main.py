from fastapi import FastAPI
from pydantic import BaseModel

from legal_rag.rag_pipeline import ask

app = FastAPI(
    title="Legal RAG API",
    version="1.0.0"
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {
        "message": "Legal RAG API running"
    }
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "Legal RAG API",
        "version": "1.0.0",
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):
    return ask(request.question)