"""
SD-01 KB Chatbot — FastAPI Backend (optional)
Run: uvicorn src.app:app --reload
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from src.rag_engine import RAGEngine
from src.ticket_service import TicketService
import uvicorn

app = FastAPI(title="SD-01 KB Chatbot API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

rag = RAGEngine(kb_path="data/kb_articles")
tickets = TicketService()


class QueryRequest(BaseModel):
    question: str


class TicketRequest(BaseModel):
    name: str
    email: str
    priority: str
    description: str
    original_question: str = ""


@app.get("/")
def root():
    return {"status": "online", "service": "SD-01 KB Chatbot", "version": "1.0.0"}


@app.post("/api/query")
async def query(req: QueryRequest):
    if not req.question.strip():
        raise HTTPException(400, "Question cannot be empty")
    result = await rag.search(req.question)
    return result


@app.post("/api/ticket")
def create_ticket(req: TicketRequest):
    ticket_id = tickets.create(req.dict())
    return {"ticket_id": ticket_id, "status": "created"}


@app.get("/api/stats")
def get_stats():
    return tickets.get_stats()


if __name__ == "__main__":
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, reload=True)
