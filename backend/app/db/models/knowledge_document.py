# backend/app/db/models/knowledge_document.py

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text
from app.db.session import Base


class KnowledgeDocument(Base):
    __tablename__ = "knowledge_documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    source_type = Column(String, nullable=False, default="guideline")
    source_name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    raw_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)