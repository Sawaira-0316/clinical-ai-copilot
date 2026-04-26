from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.session import Base


class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)

    medication_name = Column(String, nullable=False, index=True)
    dose = Column(String, nullable=True)
    route = Column(String, nullable=True)
    frequency = Column(String, nullable=True)
    status = Column(String, nullable=False, default="active")
    indication = Column(Text, nullable=True)

    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient")