from fastapi import FastAPI

from app.api.v1.health import router as health_router
from app.api.v1.chat import router as chat_router
from app.api.v1.rag import router as rag_router

app = FastAPI(
    title="KnowledgePilot AI",
    version="1.0.0",
    description="GenAI challenge project with RAG"
)

app.include_router(health_router, prefix="/api/v1")
app.include_router(chat_router, prefix="/api/v1")
app.include_router(rag_router, prefix="/api/v1")