"""
ai_engine/tools/risk_scorer.py
Calculates patient risk scores based on clinical data.
"""

from ai_engine.tools.llm_client import LLMClient


class RiskScorer:
    @staticmethod
    def calculate(
        patient: dict,
        labs: list[dict] = None,
        vitals: list[dict] = None,
        medications: list[dict] = None,
    ) -> dict:
        """
        Calculate comprehensive patient risk score.
        Returns risk level, score, and contributing factors.
        """
        risk_points = 0
        risk_factors = []
        protective_factors = []

        # Age risk
        age = patient.get("age", 0) or 0
        if age >= 75:
            risk_points += 3
            risk_factors.append("Age ≥75 (high risk)")
        elif age >= 65:
            risk_points += 2
            risk_factors.append("Age ≥65 (moderate risk)")
        elif age >= 50:
            risk_points += 1
            risk_factors.append("Age ≥50 (mild risk)")

        # Lab abnormalities
        abnormal_labs = [l for l in (labs or []) if l.get("is_abnormal")]
        risk_points += len(abnormal_labs)
        for lab in abnormal_labs:
            risk_factors.append(f"Abnormal {lab.get('lab_name')} ({lab.get('value')} {lab.get('unit', '')})")

        # Vital abnormalities
        abnormal_vitals = [v for v in (vitals or []) if v.get("is_abnormal")]
        risk_points += len(abnormal_vitals) * 2
        for vital in abnormal_vitals:
            risk_factors.append(f"Abnormal {vital.get('vital_name')} ({vital.get('value')} {vital.get('unit', '')})")

        # Polypharmacy risk
        med_count = len(medications or [])
        if med_count >= 5:
            risk_points += 2
            risk_factors.append(f"Polypharmacy ({med_count} medications)")
        elif med_count >= 3:
            risk_points += 1

        # Calculate risk level
        if risk_points >= 8:
            risk_level = "CRITICAL"
            risk_color = "🔴"
        elif risk_points >= 5:
            risk_level = "HIGH"
            risk_color = "🟠"
        elif risk_points >= 3:
            risk_level = "MODERATE"
            risk_color = "🟡"
        else:
            risk_level = "LOW"
            risk_color = "🟢"

        # Normalize score to 0-100
        normalized_score = min(int((risk_points / 15) * 100), 100)

        # AI risk narrative
        context = f"""Patient: {patient.get('name')}, Age: {age}
Risk factors: {', '.join(risk_factors) if risk_factors else 'None identified'}
Risk points: {risk_points}"""

        prompt = f"""Generate a brief clinical risk summary for this patient:
{context}

Provide:
1. Overall risk assessment (2-3 sentences)
2. Top 2 most urgent risk factors to address
3. Recommended monitoring frequency

Be concise and clinically actionable."""

        ai_narrative = LLMClient.generate(prompt, max_tokens=300)

        return {
            "patient_name": patient.get("name", "Unknown"),
            "risk_level": risk_level,
            "risk_color": risk_color,
            "risk_score": normalized_score,
            "risk_points": risk_points,
            "risk_factors": risk_factors,
            "protective_factors": protective_factors,
            "ai_narrative": ai_narrative,
            "disclaimer": "Risk score is for clinical decision support only. Clinical judgment required.",
        }

    @staticmethod
    def get_risk_badge(risk_level: str) -> str:
        badges = {
            "CRITICAL": "🔴 CRITICAL",
            "HIGH": "🟠 HIGH RISK",
            "MODERATE": "🟡 MODERATE",
            "LOW": "🟢 LOW RISK",
        }
        return badges.get(risk_level, "⚪ UNKNOWN")