# backend/app/db/repositories/knowledge_repository.py

from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.db.models.knowledge_document import KnowledgeDocument
from app.db.models.knowledge_chunk import KnowledgeChunk


class KnowledgeRepository:
    @staticmethod
    def create_document(db: Session, data: dict) -> KnowledgeDocument:
        document = KnowledgeDocument(**data)
        db.add(document)
        db.commit()
        db.refresh(document)
        return document

    @staticmethod
    def create_chunk(db: Session, data: dict) -> KnowledgeChunk:
        chunk = KnowledgeChunk(**data)
        db.add(chunk)
        db.commit()
        db.refresh(chunk)
        return chunk

    @staticmethod
    def get_chunks_by_query(db: Session, query: str):
        return (
            db.query(KnowledgeChunk)
            .filter(
                or_(
                    KnowledgeChunk.content.ilike(f"%{query}%"),
                    KnowledgeChunk.section_title.ilike(f"%{query}%"),
                )
            )
            .all()
        )