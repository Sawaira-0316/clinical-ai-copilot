# backend/app/api/v1/schemas/knowledge_vector_search.py

from pydantic import BaseModel


class KnowledgeIndexResponse(BaseModel):
    message: str
    indexed_chunks: int


class SemanticSearchRequest(BaseModel):
    query: str
    limit: int = 5


class SemanticMatchResponse(BaseModel):
    chunk_id: int
    document_id: int
    score: float
    section_title: str | None = None
    content: str


class SemanticSearchResponse(BaseModel):
    query: str
    matches: list[SemanticMatchResponse]