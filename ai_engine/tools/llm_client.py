import os
"""
ai_engine/tools/llm_client.py
LLM client using Groq with LLaMA 3.3 70B.
"""

from groq import Groq
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
MODEL = "llama-3.3-70b-versatile"


class LLMClient:
    @staticmethod
    def generate(prompt: str, system: str = None, max_tokens: int = 1024) -> str:
        """Generate a response using Groq LLaMA 3.3."""
        try:
            client = Groq(api_key=GROQ_API_KEY)

            system_message = system or (
                "You are a clinical AI assistant helping doctors review patient data. "
                "Answer based ONLY on provided evidence. "
                "Be concise, accurate, and clinically relevant. "
                "If data is missing, say so explicitly. "
                "Never make assumptions about missing data. "
                "Always remind the doctor that final medical judgment is theirs."
            )

            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content

        except Exception as e:
            return f"LLM error: {str(e)}"


class PatientAnswerPrompt:
    @staticmethod
    def build(
        question: str,
        patient_evidence: list[str],
        knowledge_evidence: list[str],
    ) -> str:
        patient_text = "\n".join(patient_evidence) if patient_evidence else "No patient data available."
        knowledge_text = "\n".join(knowledge_evidence) if knowledge_evidence else "No medical guidelines available."

        return f"""You are Clinical AI Copilot, a clinician-support assistant.

Use only the provided patient evidence and knowledge evidence.
Do not invent facts. If evidence is limited, say that clearly.
Keep the answer concise, clinically useful, and safe for review.

Question: {question}

Patient Evidence:
{patient_text}

Medical Knowledge Evidence:
{knowledge_text}

Generate a grounded, evidence-based answer for a clinician."""


