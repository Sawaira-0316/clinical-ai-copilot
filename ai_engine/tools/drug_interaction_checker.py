"""
ai_engine/tools/drug_interaction_checker.py
Checks for dangerous drug interactions in patient medications.
"""

from ai_engine.tools.llm_client import LLMClient

# Known dangerous drug combinations
KNOWN_INTERACTIONS = {
    ("warfarin", "aspirin"): {"severity": "HIGH", "effect": "Increased bleeding risk"},
    ("warfarin", "ibuprofen"): {"severity": "HIGH", "effect": "Increased bleeding risk"},
    ("warfarin", "azithromycin"): {"severity": "MODERATE", "effect": "Increased anticoagulation effect"},
    ("metformin", "contrast"): {"severity": "HIGH", "effect": "Risk of lactic acidosis"},
    ("ace inhibitor", "potassium"): {"severity": "MODERATE", "effect": "Risk of hyperkalemia"},
    ("ssri", "tramadol"): {"severity": "HIGH", "effect": "Serotonin syndrome risk"},
    ("statins", "azithromycin"): {"severity": "MODERATE", "effect": "Increased myopathy risk"},
    ("nsaid", "ace inhibitor"): {"severity": "MODERATE", "effect": "Reduced antihypertensive effect, kidney risk"},
    ("digoxin", "azithromycin"): {"severity": "HIGH", "effect": "Increased digoxin toxicity"},
    ("paracetamol", "warfarin"): {"severity": "MODERATE", "effect": "Enhanced anticoagulation at high doses"},
}


class DrugInteractionChecker:
    @staticmethod
    def check(medications: list[str]) -> dict:
        """
        Check for drug interactions in a list of medications.
        Returns found interactions with severity levels.
        """
        interactions = []
        med_lower = [m.lower() for m in medications]

        # Check known interactions
        for (drug1, drug2), info in KNOWN_INTERACTIONS.items():
            drug1_found = any(drug1 in med for med in med_lower)
            drug2_found = any(drug2 in med for med in med_lower)

            if drug1_found and drug2_found:
                interactions.append({
                    "drug1": drug1,
                    "drug2": drug2,
                    "severity": info["severity"],
                    "effect": info["effect"],
                })

        # Use AI for additional interaction checking
        if medications:
            med_list = ", ".join(medications)
            prompt = f"""Check these medications for dangerous interactions: {med_list}

List any dangerous combinations not already covered.
Format: DRUG1 + DRUG2: [SEVERITY] - [Effect]
If no additional interactions found, say "No additional interactions detected."
Be concise."""

            ai_check = LLMClient.generate(prompt, max_tokens=300)
        else:
            ai_check = "No medications to check."

        return {
            "medications_checked": medications,
            "known_interactions": interactions,
            "ai_analysis": ai_check,
            "total_interactions": len(interactions),
            "has_high_severity": any(i["severity"] == "HIGH" for i in interactions),
        }

    @staticmethod
    def format_for_display(result: dict) -> str:
        """Format interaction results for display."""
        if not result["known_interactions"]:
            return "✅ No known dangerous drug interactions detected."

        lines = ["⚠️ Drug Interactions Found:\n"]
        for interaction in result["known_interactions"]:
            severity_icon = "🔴" if interaction["severity"] == "HIGH" else "🟡"
            lines.append(
                f"{severity_icon} {interaction['drug1'].title()} + {interaction['drug2'].title()}: "
                f"[{interaction['severity']}] {interaction['effect']}"
            )
        return "\n".join(lines)