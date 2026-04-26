from sqlalchemy.orm import Session

from app.db.models.timeline_event import TimelineEvent


class TimelineRepository:
    @staticmethod
    def create(db: Session, data: dict) -> TimelineEvent:
        event = TimelineEvent(**data)
        db.add(event)
        db.commit()
        db.refresh(event)
        return event

    @staticmethod
    def get_by_patient_id(db: Session, patient_id: int):
        return (
            db.query(TimelineEvent)
            .filter(TimelineEvent.patient_id == patient_id)
            .order_by(TimelineEvent.event_time.asc())
            .all()
        )