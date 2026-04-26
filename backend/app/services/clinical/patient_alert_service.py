from sqlalchemy.orm import Session
from app.db.repositories.lab_result_repository import LabResultRepository
from app.db.repositories.vital_sign_repository import VitalSignRepository
from app.db.repositories.patient_repository import PatientRepository


class PatientAlertService:
    @staticmethod
    def get_patient_alerts(db: Session, patient_id: int) -> dict:
        patient = PatientRepository.get_by_id(db, patient_id)
        if not patient:
            raise ValueError(f"Patient {patient_id} not found.")

        alerts = []

        # Check abnormal labs
        labs = LabResultRepository.get_by_patient_id(db, patient_id)
        for lab in labs:
            if lab.is_abnormal:
                alerts.append({
                    "level": "warning",
                    "category": "lab",
                    "message": f"Abnormal lab result: {lab.lab_name} = {lab.value} {lab.unit or ''}",
                })

        # Check abnormal vitals
        vitals = VitalSignRepository.get_by_patient_id(db, patient_id)
        for vital in vitals:
            if vital.is_abnormal:
                alerts.append({
                    "level": "warning",
                    "category": "vital",
                    "message": f"Abnormal vital: {vital.vital_name} = {vital.value} {vital.unit or ''}",
                })

        if not alerts:
            alerts.append({
                "level": "info",
                "category": "general",
                "message": "No critical alerts detected for this patient.",
            })

        return {
            "patient_id": patient_id,
            "alerts": alerts,
            "total": len(alerts),
        }