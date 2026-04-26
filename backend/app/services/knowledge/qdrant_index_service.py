from sqlalchemy.orm import Session


class QdrantIndexService:
    """Stub — Qdrant vector indexing coming in Phase 4."""

    @staticmethod
    def index_knowledge_chunks(db: Session) -> dict:
        return {
            "status": "pending",
            "message": "Qdrant vector indexing will be enabled in Phase 4.",
            "chunks_indexed": 0,
        }

    @staticmethod
    def semantic_search(query: str, limit: int = 5) -> dict:
        return {
            "query": query,
            "results": [],
            "message": "Semantic search (Qdrant) coming in Phase 4.",
        }