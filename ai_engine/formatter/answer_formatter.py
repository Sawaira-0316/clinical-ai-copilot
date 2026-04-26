"""
ai_engine/formatter/answer_formatter.py
Formats the final clinical AI response.
"""


class AnswerFormatter:
    @staticmethod
    def format(
        question: str,
        answer: str,
        patient_evidence: list[str],
        knowledge_evidence: list[str],
        source_sections: list[str],
        citations: list[str],
        confidence: float,
    ) -> dict:
        """Format the complete clinical response."""
        return {
            "answer": answer,
            "citations": citations,
            "confidence": confidence,
            "confidence_label": AnswerFormatter._confidence_label(confidence),
            "sources_used": {
                "patient_data": len(patient_evidence) > 0,
                "knowledge_base": len(knowledge_evidence) > 0,
                "source_sections": source_sections,
            },
            "metadata": {
                "patient_evidence_count": len(patient_evidence),
                "knowledge_evidence_count": len(knowledge_evidence),
            },
        }

    @staticmethod
    def _confidence_label(confidence: float) -> str:
        if confidence >= 0.8:
            return "High"
        elif confidence >= 0.5:
            return "Medium"
        elif confidence >= 0.3:
            return "Low"
        else:
            return "Very Low"