# backend/app/api/v1/routes/knowledge_base.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.schemas.knowledge_base import (
    KnowledgeDocumentCreate,
    KnowledgeDocumentResponse,
    KnowledgeSearchRequest,
    KnowledgeSearchResponse,
)
from app.db.session import get_db
from app.services.knowledge.knowledge_service import KnowledgeService

router = APIRouter()


@router.post("/knowledge/documents", response_model=KnowledgeDocumentResponse, tags=["Knowledge Base"])
def create_knowledge_document(
    payload: KnowledgeDocumentCreate,
    db: Session = Depends(get_db),
):
    try:
        return KnowledgeService.create_knowledge_document(db, payload.model_dump())
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to create knowledge document: {str(exc)}")


@router.post("/knowledge/search", response_model=KnowledgeSearchResponse, tags=["Knowledge Base"])
def search_knowledge(
    payload: KnowledgeSearchRequest,
    db: Session = Depends(get_db),
):
    try:
        return KnowledgeService.search_knowledge(db, payload.query)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to search knowledge base: {str(exc)}")