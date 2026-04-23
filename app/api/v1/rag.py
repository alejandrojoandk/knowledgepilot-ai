from fastapi import APIRouter, HTTPException

from app.schemas.rag import RagRequest, RagResponse
from app.services.rag_service import rag_service

router = APIRouter(tags=["rag"])


@router.post("/rag-query", response_model=RagResponse)
def rag_query(payload: RagRequest):
    try:
        return rag_service.ask(
            query=payload.query,
            top_k=payload.top_k
        )

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))