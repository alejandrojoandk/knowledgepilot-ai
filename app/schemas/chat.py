from typing import Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    session_id: Optional[str] = None
    model_name: Optional[str] = None


class ChatMeta(BaseModel):
    latency_ms: int
    model: str


class ChatResponse(BaseModel):
    reply: str
    meta: ChatMeta