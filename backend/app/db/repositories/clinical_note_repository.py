from sqlalchemy.orm import Session

from app.db.models.clinical_note import ClinicalNote


class ClinicalNoteRepository:
    @staticmethod
    def create(db: Session, data: dict) -> ClinicalNote:
        note = ClinicalNote(**data)
        db.add(note)
        db.commit()
        db.refresh(note)
        return note

    @staticmethod
    def get_by_patient_id(db: Session, patient_id: int):
        return (
            db.query(ClinicalNote)
            .filter(ClinicalNote.patient_id == patient_id)
            .order_by(ClinicalNote.note_time.asc())
            .all()
        )