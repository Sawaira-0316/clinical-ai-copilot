from groq import Groq
import os
from sqlalchemy.orm import Session
from app.db.repositories.patient_repository import PatientRepository
from app.db.repositories.lab_result_repository import LabResultRepository
from app.db.repositories.vital_sign_repository import VitalSignRepository
from app.db.repositories.medication_repository import MedicationRepository
from app.db.repositories.clinical_note_repository import ClinicalNoteRepository

from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class PatientSummaryService:
    @staticmethod
    def get_patient_summary(db: Session, patient_id: int) -> dict:
        patient = PatientRepository.get_by_id(db, patient_id)
        if not patient:
            return {"patient_id": patient_id, "summary": "Patient not found.", "generated_at": None}

        labs = LabResultRepository.get_by_patient_id(db, patient_id)
        vitals = VitalSignRepository.get_by_patient_id(db, patient_id)
        medications = MedicationRepository.get_by_patient_id(db, patient_id)
        notes = ClinicalNoteRepository.get_by_patient_id(db, patient_id)

        context = (
            f"Patient: {patient.name}, Age: {patient.age}, Gender: {patient.gender}. "
            f"Labs: {len(labs)}, Vitals: {len(vitals)}, "
            f"Medications: {len(medications)}, Notes: {len(notes)}"
        )

        try:
            client = Groq(api_key=GROQ_API_KEY)
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a clinical AI assistant. Generate a concise patient summary based only on provided data."},
                    {"role": "user", "content": f"Generate clinical summary for: {context}"}
                ],
                max_tokens=512,
            )
            summary = response.choices[0].message.content
        except Exception as e:
            summary = f"Summary error: {str(e)}"

        return {"patient_id": patient_id, "summary": summary, "generated_at": None}