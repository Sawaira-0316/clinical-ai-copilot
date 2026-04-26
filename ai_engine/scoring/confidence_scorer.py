"""
ai_engine/scoring/confidence_scorer.py
Scores confidence based on evidence quality and quantity.
"""


class ConfidenceScorer:
    @staticmethod
    def score(
        patient_evidence: list[str],
        knowledge_evidence: list[str],
    ) -> float:
        """
        Score confidence from 0.0 to 1.0 based on evidence.
        - Patient evidence available: +0.4
        - Knowledge evidence available: +0.4
        - Both available: +0.2 bonus
        """
        score = 0.0

        has_patient = bool(patient_evidence and patient_evidence != ["No patient data available."])
        has_knowledge = bool(knowledge_evidence and knowledge_evidence != ["No medical guidelines available."])

        if has_patient:
            score += 0.4
        if has_knowledge:
            score += 0.4
        if has_patient and has_knowledge:
            score += 0.2

        return round(min(score, 1.0), 2)