from fastapi import APIRouter, HTTPException

from app.schemas.rag import RagRequest, RagResponse
from app.services.rag_service import get_rag_service
from app.services.llm_service import llm_service

router = APIRouter()


@router.post("/rag-query", response_model=RagResponse)
def rag_query(payload: RagRequest):
    try:
        rag_service = get_rag_service()

        context, sources = rag_service.query(
            question=payload.query,
            top_k=payload.top_k,
        )

        prompt = f"""
You are a helpful assistant.

Answer ONLY using the provided context.
If the answer is not contained in the context, say you don't know.

Context:
{context}

Question:
{payload.query}
"""

        answer = llm_service.ask(prompt)

        return RagResponse(
            answer=answer,
            sources=sources,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))