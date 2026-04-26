from sqlalchemy.orm import Session
from app.db.models.vital_sign import VitalSign


class VitalSignRepository:
    @staticmethod
    def create(db: Session, data: dict) -> VitalSign:
        vital = VitalSign(**data)
        db.add(vital)
        db.commit()
        db.refresh(vital)
        return vital

    @staticmethod
    def get_by_patient_id(db: Session, patient_id: int):
        return (
            db.query(VitalSign)
            .filter(VitalSign.patient_id == patient_id)
            .order_by(VitalSign.measured_at.asc())
            .all()
        )