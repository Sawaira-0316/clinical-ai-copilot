# backend/app/db/models/knowledge_chunk.py

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from app.db.session import Base


class KnowledgeChunk(Base):
    __tablename__ = "knowledge_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("knowledge_documents.id"), nullable=False, index=True)
    chunk_index = Column(Integer, nullable=False)
    section_title = Column(String, nullable=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)