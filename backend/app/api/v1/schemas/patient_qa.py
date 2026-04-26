from pydantic import BaseModel


class PatientQuestionRequest(BaseModel):
    question: str


class PatientQuestionResponse(BaseModel):
    question: str
    answer: str
    patient_evidence: list[str]
    knowledge_evidence: list[str]
    source_sections: list[str]
    safety_note: str