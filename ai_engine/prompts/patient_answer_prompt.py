"""
ai_engine/prompts/patient_answer_prompt.py
Clinical prompt templates for the AI agent.
"""


class PatientAnswerPrompt:
    @staticmethod
    def build(
        question: str,
        patient_evidence: list[str],
        knowledge_evidence: list[str],
    ) -> str:
        """Build the clinical Q&A prompt."""
        patient_text = "\n".join(patient_evidence) if patient_evidence else "No patient data available."
        knowledge_text = "\n".join(knowledge_evidence) if knowledge_evidence else "No medical guidelines found in knowledge base."

        return f"""You are Clinical AI Copilot, an evidence-based clinical support assistant.

IMPORTANT RULES:
- Answer ONLY based on the provided evidence below
- Do NOT invent or assume missing information
- If evidence is insufficient, clearly state what is missing
- Be concise and clinically relevant
- Always remind the clinician that final judgment is theirs

CLINICAL QUESTION:
{question}

PATIENT EVIDENCE (from EHR):
{patient_text}

MEDICAL KNOWLEDGE EVIDENCE (from Clinical Guidelines):
{knowledge_text}

Provide a structured, evidence-based clinical response:"""

    @staticmethod
    def build_summary_prompt(patient_context: str) -> str:
        """Build a patient summary prompt."""
        return f"""You are a clinical AI assistant generating a patient summary for a doctor.

Generate a concise, structured clinical summary based ONLY on the data below.

Format:
1. Patient Overview
2. Key Clinical Findings
3. Current Medications
4. Recommendations for Review

PATIENT DATA:
{patient_context}

Generate the clinical summary:"""