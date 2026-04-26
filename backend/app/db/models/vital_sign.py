from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from app.db.session import Base


class VitalSign(Base):
    __tablename__ = "vital_signs"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    vital_name = Column(String, nullable=False, index=True)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=True)
    is_abnormal = Column(Boolean, default=False)
    measured_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient")