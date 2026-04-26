from sqlalchemy.orm import Session
from app.db.repositories.knowledge_repository import KnowledgeRepository


class KnowledgeService:
    @staticmethod
    def create_knowledge_document(db: Session, data: dict):
        return KnowledgeRepository.create_document(db, data)

    @staticmethod
    def search_knowledge(db: Session, query: str) -> dict:
        chunks = KnowledgeRepository.get_chunks_by_query(db, query)
        return {
            "query": query,
            "results": [
                {
                    "chunk_id": c.id,
                    "document_id": c.document_id,
                    "section_title": c.section_title,
                    "content": c.content[:500],
                }
                for c in chunks
            ],
            "total": len(chunks),
        }