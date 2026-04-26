"""
ai_engine/safety/answer_guard.py
Safety filter to ensure clinical AI answers are safe and appropriate.
"""


class AnswerGuard:
    UNSAFE_PHRASES = [
        "you should take",
        "i recommend taking",
        "definitely take",
        "you must take",
        "prescribe",
        "i diagnose",
        "you have",
        "you definitely have",
    ]

    DISCLAIMER = (
        "\n\n⚠️ *This is an AI-generated clinical support response. "
        "Final medical judgment must be made by a qualified clinician.*"
    )

    @staticmethod
    def apply(
        answer: str,
        patient_evidence: list[str],
        knowledge_evidence: list[str],
    ) -> str:
        """Apply safety checks and add disclaimer."""
        if not answer:
            return "Unable to generate a safe answer based on available evidence."

        # Check for unsafe content
        answer_lower = answer.lower()
        for phrase in AnswerGuard.UNSAFE_PHRASES:
            if phrase in answer_lower:
                answer = answer + "\n\n*Note: Please verify this recommendation with clinical judgment.*"
                break

        # Always add disclaimer
        answer = answer + AnswerGuard.DISCLAIMER

        return answer