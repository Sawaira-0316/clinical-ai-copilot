"""
Script to populate Qdrant with clinical medical knowledge.
Run from: E:\Clinical AI Copilot
Command: python add_medical_knowledge.py
"""

import sys
import os
sys.path.insert(0, "E:\\Clinical AI Copilot")

from ai_engine.embeddings.qdrant_service import store_document_chunks, ensure_collection

# ── Clinical Medical Knowledge ────────────────────────────────────────────────

MEDICAL_KNOWLEDGE = [
    {
        "source": "Clinical Guidelines - Lab Values",
        "section_title": "Normal Lab Reference Ranges",
        "text": """Normal laboratory reference ranges for adults:
- Creatinine: 0.6-1.2 mg/dL (men), 0.5-1.1 mg/dL (women). Elevated creatinine indicates kidney dysfunction.
- WBC (White Blood Cells): 4.5-11.0 K/uL. Elevated WBC indicates infection or inflammation.
- Hemoglobin: 13.5-17.5 g/dL (men), 12.0-15.5 g/dL (women). Low hemoglobin indicates anemia.
- Sodium: 136-145 mmol/L. Abnormal sodium indicates electrolyte imbalance.
- Potassium: 3.5-5.0 mmol/L. Abnormal potassium can cause cardiac arrhythmias.
- Glucose: 70-100 mg/dL (fasting). Elevated glucose indicates diabetes or hyperglycemia.
- HbA1c: <5.7% normal, 5.7-6.4% prediabetes, ≥6.5% diabetes."""
    },
    {
        "source": "Clinical Guidelines - Vital Signs",
        "section_title": "Normal Vital Signs Reference",
        "text": """Normal vital signs for adults:
- Heart Rate: 60-100 bpm. Tachycardia (>100 bpm) may indicate infection, dehydration, or cardiac issues.
- Blood Pressure: <120/80 mmHg normal. Hypertension defined as >140/90 mmHg.
- Temperature: 36.1-37.2°C (97-99°F). Fever >38°C (100.4°F) indicates infection.
- Respiratory Rate: 12-20 breaths/min. Tachypnea (>20) may indicate respiratory distress.
- Oxygen Saturation: >95%. SpO2 <90% requires immediate intervention.
- BMI: 18.5-24.9 normal, 25-29.9 overweight, >30 obese."""
    },
    {
        "source": "Clinical Guidelines - Kidney Function",
        "section_title": "Acute Kidney Injury Assessment",
        "text": """Acute Kidney Injury (AKI) assessment:
- Elevated creatinine (>1.2 mg/dL men, >1.1 mg/dL women) warrants investigation.
- eGFR < 60 mL/min/1.73m² indicates chronic kidney disease.
- Monitor urine output: oliguria defined as <0.5 mL/kg/hr for 6+ hours.
- Common causes: dehydration, nephrotoxic medications, sepsis, obstruction.
- Management: IV fluids if hypovolemic, discontinue nephrotoxic drugs, nephrology consult if severe.
- Medications requiring dose adjustment in renal impairment: metformin, NSAIDs, aminoglycosides."""
    },
    {
        "source": "Clinical Guidelines - Infection",
        "section_title": "Sepsis Recognition and Management",
        "text": """Sepsis recognition criteria (qSOFA):
- Respiratory rate ≥22/min
- Altered mentation
- Systolic BP ≤100 mmHg
Signs of infection: fever >38°C, WBC >11 K/uL or <4 K/uL, elevated CRP/procalcitonin.
Management: Blood cultures before antibiotics, broad-spectrum antibiotics within 1 hour,
IV fluid resuscitation 30 mL/kg if hypotensive, monitor lactate, ICU if refractory shock."""
    },
    {
        "source": "Clinical Guidelines - Medications",
        "section_title": "Common Clinical Medications",
        "text": """Common clinical medications and considerations:
- Paracetamol (Acetaminophen): Max 4g/day, reduce in liver disease. Used for pain and fever.
- Azithromycin: Antibiotic for respiratory infections. Monitor QT prolongation.
- Metformin: First-line diabetes. Hold if eGFR <30, contrast procedures.
- Aspirin: Antiplatelet. Avoid with active bleeding, ulcers.
- Beta-blockers: Heart rate control. Do not abruptly stop — risk of rebound hypertension.
- ACE inhibitors: Hypertension, heart failure. Monitor potassium, creatinine.
Drug interactions to monitor: warfarin with antibiotics, statins with azithromycin."""
    },
    {
        "source": "Clinical Guidelines - Cardiac",
        "section_title": "Cardiac Assessment",
        "text": """Cardiac assessment guidelines:
- Hypertension: BP >140/90 mmHg. First-line: lifestyle modification, ACE inhibitors, or calcium channel blockers.
- Tachycardia (HR >100 bpm): Assess for pain, fever, dehydration, anxiety, medications, thyroid disease.
- Bradycardia (HR <60 bpm): Assess medications (beta-blockers, digoxin), electrolytes, hypothyroidism.
- Chest pain evaluation: ECG within 10 minutes, troponin levels, clinical history.
- Heart failure signs: dyspnea, orthopnea, peripheral edema, elevated BNP."""
    },
    {
        "source": "Clinical Guidelines - Diabetes",
        "section_title": "Diabetes Management",
        "text": """Diabetes management guidelines:
- Type 2 Diabetes: HbA1c target <7% for most patients.
- Hypoglycemia: Blood glucose <70 mg/dL. Treat with 15g fast-acting carbohydrates.
- Hyperglycemia: Blood glucose >180 mg/dL postprandial warrants treatment adjustment.
- Monitoring: HbA1c every 3 months until stable, then every 6 months.
- Complications screening: Annual eye exam, foot exam, urine albumin, kidney function.
- Metformin: First-line unless contraindicated. Add GLP-1 or SGLT2 inhibitor if needed."""
    },
    {
        "source": "Clinical Guidelines - Respiratory",
        "section_title": "Respiratory Assessment",
        "text": """Respiratory assessment guidelines:
- Normal SpO2: 95-100%. Values <90% require supplemental oxygen.
- Pneumonia signs: fever, cough, consolidation on chest X-ray, elevated WBC.
- COPD exacerbation: increased dyspnea, sputum, wheezing. Treatment: bronchodilators, steroids, antibiotics.
- Asthma: reversible airflow obstruction. Triggered by allergens, exercise, cold air.
- Respiratory rate >20/min is tachypnea — investigate cause.
- Pulse oximetry: reliable indicator of oxygenation. Unreliable with carbon monoxide poisoning."""
    },
]


def main():
    print("🏥 Clinical AI Copilot — Medical Knowledge Ingestion")
    print("=" * 55)

    ensure_collection()
    print(f"✅ Qdrant collection ready")

    total_chunks = 0
    for doc in MEDICAL_KNOWLEDGE:
        chunks = [doc]  # Each document is one chunk for now
        stored = store_document_chunks(chunks)
        total_chunks += stored
        print(f"✅ Stored: {doc['section_title']} ({stored} chunk)")

    print("=" * 55)
    print(f"✅ Total chunks stored in Qdrant: {total_chunks}")
    print("🚀 RAG is ready! Ask clinical questions to see evidence-based answers.")


if __name__ == "__main__":
    main()