# backend/app/core/qdrant_client.py

from qdrant_client import QdrantClient

from app.core.config import settings


def get_qdrant_client():
    return QdrantClient(
        host=settings.QDRANT_HOST,
        port=settings.QDRANT_PORT,
    )