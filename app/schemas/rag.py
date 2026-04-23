from typing import Optional, List
from pydantic import BaseModel, Field


class RagRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=4000)
    top_k: Optional[int] = 3


class SourceItem(BaseModel):
    source: str
    chunk_id: int


class RagResponse(BaseModel):
    answer: str
    sources: List[SourceItem]