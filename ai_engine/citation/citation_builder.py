"""
ai_engine/citation/citation_builder.py
Builds citations from patient and knowledge evidence.
"""


class CitationBuilder:
    @staticmethod
    def build(
        patient_evidence: list[str],
        knowledge_evidence: list[str],
    ) -> list[str]:
        """Build citation list from evidence sources."""
        citations = []

        if patient_evidence and patient_evidence != ["No patient data available."]:
            citations.append("Patient Electronic Health Record (EHR)")

        if knowledge_evidence and knowledge_evidence != ["No medical guidelines available."]:
            citations.append("Clinical Knowledge Base (Qdrant RAG)")

        if not citations:
            citations.append("No sources available")

        return citations