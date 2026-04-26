# backend/app/api/v1/routes/knowledge_vector.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.schemas.knowledge_vector_search import (
    KnowledgeIndexResponse,
    SemanticSearchRequest,
    SemanticSearchResponse,
)
from app.db.session import get_db
from app.services.knowledge.qdrant_index_service import QdrantIndexService

router = APIRouter()


@router.post("/knowledge/index", response_model=KnowledgeIndexResponse, tags=["Knowledge Vector"])
def index_knowledge(db: Session = Depends(get_db)):
    try:
        return QdrantIndexService.index_knowledge_chunks(db)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to index knowledge chunks: {str(exc)}")


@router.post("/knowledge/semantic-search", response_model=SemanticSearchResponse, tags=["Knowledge Vector"])
def semantic_search(
    payload: SemanticSearchRequest,
    db: Session = Depends(get_db),
):
    try:
        return QdrantIndexService.semantic_search(payload.query, payload.limit)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed semantic search: {str(exc)}")