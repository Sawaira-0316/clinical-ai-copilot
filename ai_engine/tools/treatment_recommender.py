"""
ai_engine/tools/treatment_recommender.py
Generates evidence-based treatment recommendations.
"""

from ai_engine.tools.llm_client import LLMClient


class TreatmentRecommender:
    @staticmethod
    def recommend(
        patient_context: str,
        diagnosis: str = None,
        labs: list[dict] = None,
        medications: list[dict] = None,
    ) -> dict:
        """
        Generate treatment recommendations based on patient data.
        """
        lab_text = "\n".join([
            f"- {l.get('lab_name')}: {l.get('value')} {l.get('unit', '')} "
            f"({'ABNORMAL' if l.get('is_abnormal') else 'normal'})"
            for l in (labs or [])
        ]) or "No lab data"

        med_text = "\n".join([
            f"- {m.get('medication_name')} {m.get('dose', '')} {m.get('frequency', '')}"
            for m in (medications or [])
        ]) or "No current medications"

        diagnosis_text = diagnosis or "Not specified — generate general recommendations based on data"

        prompt = f"""Generate evidence-based treatment recommendations for this patient:

Patient Context: {patient_context}
Working Diagnosis: {diagnosis_text}

Current Lab Results:
{lab_text}

Current Medications:
{med_text}

Provide recommendations in this format:
**Immediate Actions:**
- [Action 1]
- [Action 2]

**Medication Adjustments:**
- [Adjustment 1]

**Monitoring Plan:**
- [What to monitor]
- [Frequency]

**Follow-up:**
- [Timeline and specialist referrals if needed]

Base ONLY on provided evidence. Flag any drug interactions or contraindications.
End with: "⚠️ These recommendations require physician review before implementation."
"""

        recommendations = LLMClient.generate(prompt, max_tokens=700)

        return {
            "recommendations": recommendations,
            "diagnosis": diagnosis_text,
            "based_on": {
                "labs_count": len(labs or []),
                "medications_count": len(medications or []),
            },
            "disclaimer": "AI-generated recommendations for clinical decision support only. Must be reviewed by a qualified physician.",
        }