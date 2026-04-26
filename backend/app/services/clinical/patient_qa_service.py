"""
backend/app/services/clinical/patient_qa_service.py
Patient Q&A using complete LangGraph agent with all tools.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../../../"))

from sqlalchemy.orm import Session
from app.db.repositories.patient_repository import PatientRepository
from app.db.repositories.lab_result_repository import LabResultRepository
from app.db.repositories.vital_sign_repository import VitalSignRepository
from app.db.repositories.medication_repository import MedicationRepository
from app.db.repositories.clinical_note_repository import ClinicalNoteRepository


class PatientQAService:
    @staticmethod
    def ask_question(patient_id: int, question: str, db: Session) -> dict:
        patient = PatientRepository.get_by_id(db, patient_id)
        if not patient:
            return {"patient_id": patient_id, "question": question, "answer": f"Patient {patient_id} not found.", "sources": [], "confidence": 0.0}

        labs = LabResultRepository.get_by_patient_id(db, patient_id)
        vitals = VitalSignRepository.get_by_patient_id(db, patient_id)
        medications = MedicationRepository.get_by_patient_id(db, patient_id)
        notes = ClinicalNoteRepository.get_by_patient_id(db, patient_id)

        # Build patient data dicts for agent tools
        labs_data = [{"lab_name": l.lab_name, "value": l.value, "unit": l.unit, "is_abnormal": l.is_abnormal, "measured_at": str(l.measured_at)} for l in labs]
        vitals_data = [{"vital_name": v.vital_name, "value": v.value, "unit": v.unit, "is_abnormal": v.is_abnormal, "measured_at": str(v.measured_at)} for v in vitals]
        meds_data = [{"medication_name": m.medication_name, "dose": m.dose, "frequency": m.frequency, "status": m.status} for m in medications]
        patient_dict = {"name": patient.name, "age": patient.age, "gender": patient.gender}

        # Build context string
        lab_text = "\n".join([f"- {l['lab_name']}: {l['value']} {l['unit'] or ''} ({'ABNORMAL' if l['is_abnormal'] else 'normal'})" for l in labs_data]) or "No lab data."
        vital_text = "\n".join([f"- {v['vital_name']}: {v['value']} {v['unit'] or ''} ({'ABNORMAL' if v['is_abnormal'] else 'normal'})" for v in vitals_data]) or "No vitals data."
        med_text = "\n".join([f"- {m['medication_name']} {m['dose'] or ''} {m['frequency'] or ''}" for m in meds_data]) or "No medications."
        note_text = "\n".join([f"- {n.title}: {n.content[:300]}" for n in notes]) or "No clinical notes."

        patient_context = (
            f"Patient: {patient.name}, Age: {patient.age}, Gender: {patient.gender}\n\n"
            f"Labs ({len(labs)} records):\n{lab_text}\n\n"
            f"Vitals ({len(vitals)} records):\n{vital_text}\n\n"
            f"Medications ({len(medications)} records):\n{med_text}\n\n"
            f"Notes ({len(notes)} records):\n{note_text}"
        )

        try:
            from ai_engine.workflows.patient_answer_workflow import PatientAnswerWorkflow
            result = PatientAnswerWorkflow.run(
                question=question,
                patient_evidence=[patient_context],
                knowledge_evidence=[],
                source_sections=[],
                patient_context=patient_context,
                patient=patient_dict,
                labs=labs_data,
                vitals=vitals_data,
                medications=meds_data,
            )
            answer = result.get("answer", "No answer generated.")
            citations = result.get("citations", [])
            confidence = result.get("confidence", 0.0)
            drug_interactions = result.get("drug_interactions", {})
            lab_analysis = result.get("lab_analysis", {})
            risk_assessment = result.get("risk_assessment", {})

        except Exception as e:
            print(f"Agent error: {e}, falling back to direct Groq")
            from groq import Groq
            GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
            client = Groq(api_key=GROQ_API_KEY)
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a clinical AI assistant. Answer based ONLY on provided patient data."},
                    {"role": "user", "content": f"Patient Data:\n{patient_context}\n\nQuestion: {question}"}
                ],
                max_tokens=1024,
            )
            answer = response.choices[0].message.content
            citations = []
            confidence = 0.4
            drug_interactions = {}
            lab_analysis = {}
            risk_assessment = {}

        return {
            "patient_id": patient_id,
            "patient_name": patient.name,
            "question": question,
            "answer": answer,
            "sources": citations,
            "confidence": confidence,
            "drug_interactions": drug_interactions,
            "lab_analysis": lab_analysis,
            "risk_assessment": risk_assessment,
        }


