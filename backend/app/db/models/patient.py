from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from app.db.session import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)