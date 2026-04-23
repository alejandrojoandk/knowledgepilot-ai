from fastapi import APIRouter, HTTPException

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.llm_service import llm_service

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    try:
        result = llm_service.chat(
            message=payload.message,
            model_name=payload.model_name
        )

        return {
            "reply": result["reply"],
            "meta": {
                "latency_ms": result["latency_ms"],
                "model": result["model"],
            },
        }

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))