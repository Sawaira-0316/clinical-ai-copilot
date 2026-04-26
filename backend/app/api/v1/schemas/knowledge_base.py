# backend/app/api/v1/schemas/knowledge_base.py

from pydantic import BaseModel


class KnowledgeDocumentCreate(BaseModel):
    title: str
    source_type: str = "guideline"
    source_name: str | None = None
    description: str | None = None
    raw_text: str


class KnowledgeDocumentResponse(BaseModel):
    id: int
    title: str
    source_type: str
    source_name: str | None = None
    description: str | None = None
    raw_text: str

    class Config:
        from_attributes = True


class KnowledgeChunkResponse(BaseModel):
    id: int
    document_id: int
    chunk_index: int
    section_title: str | None = None
    content: str

    class Config:
        from_attributes = True


class KnowledgeSearchRequest(BaseModel):
    query: str


class KnowledgeSearchResponse(BaseModel):
    query: str
    matches: list[KnowledgeChunkResponse]