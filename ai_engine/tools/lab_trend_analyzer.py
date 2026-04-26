"""
ai_engine/tools/lab_trend_analyzer.py
Analyzes lab result trends over time to detect patterns.
"""

from ai_engine.tools.llm_client import LLMClient


class LabTrendAnalyzer:
    # Normal ranges for common labs
    NORMAL_RANGES = {
        "creatinine": {"min": 0.6, "max": 1.2, "unit": "mg/dL", "concern": "kidney"},
        "wbc": {"min": 4.5, "max": 11.0, "unit": "K/uL", "concern": "infection"},
        "hemoglobin": {"min": 12.0, "max": 17.5, "unit": "g/dL", "concern": "anemia"},
        "sodium": {"min": 136, "max": 145, "unit": "mmol/L", "concern": "electrolyte"},
        "potassium": {"min": 3.5, "max": 5.0, "unit": "mmol/L", "concern": "cardiac"},
        "glucose": {"min": 70, "max": 100, "unit": "mg/dL", "concern": "diabetes"},
        "hba1c": {"min": 0, "max": 5.7, "unit": "%", "concern": "diabetes"},
    }

    @staticmethod
    def analyze(labs: list[dict]) -> dict:
        """
        Analyze lab results for trends and abnormalities.
        Labs should have: lab_name, value, unit, measured_at, is_abnormal
        """
        if not labs:
            return {
                "summary": "No lab data available for analysis.",
                "abnormal_labs": [],
                "trends": [],
                "risk_flags": [],
                "ai_interpretation": "No lab data to analyze.",
            }

        abnormal_labs = []
        risk_flags = []
        lab_groups = {}

        # Group labs by name for trend analysis
        for lab in labs:
            name = lab.get("lab_name", "").lower()
            if name not in lab_groups:
                lab_groups[name] = []
            lab_groups[name].append(lab)

            # Check if abnormal
            if lab.get("is_abnormal"):
                abnormal_labs.append({
                    "name": lab.get("lab_name"),
                    "value": lab.get("value"),
                    "unit": lab.get("unit", ""),
                    "date": str(lab.get("measured_at", "")),
                })

                # Check for critical values
                for key, ranges in LabTrendAnalyzer.NORMAL_RANGES.items():
                    if key in name:
                        value = float(lab.get("value", 0))
                        if value > ranges["max"] * 1.5:
                            risk_flags.append(
                                f"CRITICAL: {lab.get('lab_name')} severely elevated — "
                                f"possible {ranges['concern']} issue"
                            )

        # Detect trends (rising/falling)
        trends = []
        for lab_name, values in lab_groups.items():
            if len(values) >= 2:
                sorted_values = sorted(values, key=lambda x: str(x.get("measured_at", "")))
                first = float(sorted_values[0].get("value", 0))
                last = float(sorted_values[-1].get("value", 0))

                if last > first * 1.2:
                    trends.append(f"📈 {lab_name.title()} is RISING ({first} → {last})")
                elif last < first * 0.8:
                    trends.append(f"📉 {lab_name.title()} is FALLING ({first} → {last})")

        # AI interpretation
        lab_summary = "\n".join([
            f"- {l.get('lab_name')}: {l.get('value')} {l.get('unit', '')} "
            f"({'ABNORMAL' if l.get('is_abnormal') else 'normal'})"
            for l in labs
        ])

        prompt = f"""Interpret these lab results clinically:
{lab_summary}

Provide:
1. Key clinical concerns
2. Most urgent abnormality to address
3. Recommended follow-up tests
Be concise and clinically focused."""

        ai_interpretation = LLMClient.generate(prompt, max_tokens=400)

        return {
            "total_labs": len(labs),
            "abnormal_labs": abnormal_labs,
            "abnormal_count": len(abnormal_labs),
            "trends": trends,
            "risk_flags": risk_flags,
            "ai_interpretation": ai_interpretation,
            "summary": f"{len(abnormal_labs)} abnormal values out of {len(labs)} lab results.",
        }