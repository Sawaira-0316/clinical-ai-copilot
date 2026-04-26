"""
ai_engine/workflows/patient_answer_workflow.py
Complete LangGraph agentic workflow with all clinical tools.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END

from ai_engine.prompts.patient_answer_prompt import PatientAnswerPrompt
from ai_engine.tools.llm_client import LLMClient
from ai_engine.retrieval.rag_retriever import RAGRetriever
from ai_engine.safety.answer_guard import AnswerGuard
from ai_engine.citation.citation_builder import CitationBuilder
from ai_engine.scoring.confidence_scorer import ConfidenceScorer
from ai_engine.formatter.answer_formatter import AnswerFormatter
from ai_engine.tools.drug_interaction_checker import DrugInteractionChecker
from ai_engine.tools.lab_trend_analyzer import LabTrendAnalyzer
from ai_engine.tools.risk_scorer import RiskScorer


class ClinicalAgentState(TypedDict):
    question: str
    patient_context: str
    patient: dict
    labs: list
    vitals: list
    medications: list
    patient_evidence: list
    knowledge_evidence: list
    source_sections: list
    drug_interactions: dict
    lab_analysis: dict
    risk_assessment: dict
    raw_answer: str
    safe_answer: str
    citations: list
    confidence: float
    final_response: dict


def retrieve_knowledge(state: ClinicalAgentState) -> ClinicalAgentState:
    query = f"{state['question']} {state.get('patient_context', '')}"[:500]
    chunks = RAGRetriever.retrieve(query, top_k=5)
    return {
        **state,
        "knowledge_evidence": [c["text"] for c in chunks],
        "source_sections": [f"{c.get('source')} - {c.get('section_title')}" for c in chunks],
    }


def check_drug_interactions(state: ClinicalAgentState) -> ClinicalAgentState:
    medications = state.get("medications", [])
    med_names = [m.get("medication_name", "") for m in medications if m.get("medication_name")]
    if med_names:
        result = DrugInteractionChecker.check(med_names)
    else:
        result = {"known_interactions": [], "ai_analysis": "No medications to check.", "total_interactions": 0, "has_high_severity": False}
    return {**state, "drug_interactions": result}


def analyze_labs(state: ClinicalAgentState) -> ClinicalAgentState:
    result = LabTrendAnalyzer.analyze(state.get("labs", []))
    return {**state, "lab_analysis": result}


def assess_risk(state: ClinicalAgentState) -> ClinicalAgentState:
    result = RiskScorer.calculate(
        patient=state.get("patient", {}),
        labs=state.get("labs", []),
        vitals=state.get("vitals", []),
        medications=state.get("medications", []),
    )
    return {**state, "risk_assessment": result}


def build_patient_evidence(state: ClinicalAgentState) -> ClinicalAgentState:
    evidence = []
    if state.get("patient_context"):
        evidence.append(state["patient_context"])
    if state.get("drug_interactions", {}).get("known_interactions"):
        evidence.append(DrugInteractionChecker.format_for_display(state["drug_interactions"]))
    if state.get("lab_analysis", {}).get("risk_flags"):
        evidence.extend(state["lab_analysis"]["risk_flags"])
    if state.get("risk_assessment", {}).get("risk_level"):
        risk = state["risk_assessment"]
        evidence.append(f"Risk Level: {risk.get('risk_color')} {risk.get('risk_level')} (Score: {risk.get('risk_score')}/100)")
    return {**state, "patient_evidence": evidence}


def generate_answer(state: ClinicalAgentState) -> ClinicalAgentState:
    prompt = PatientAnswerPrompt.build(
        question=state["question"],
        patient_evidence=state.get("patient_evidence", []),
        knowledge_evidence=state.get("knowledge_evidence", []),
    )
    return {**state, "raw_answer": LLMClient.generate(prompt)}


def apply_safety(state: ClinicalAgentState) -> ClinicalAgentState:
    return {**state, "safe_answer": AnswerGuard.apply(state["raw_answer"], state.get("patient_evidence", []), state.get("knowledge_evidence", []))}


def build_citations(state: ClinicalAgentState) -> ClinicalAgentState:
    return {**state, "citations": CitationBuilder.build(state.get("patient_evidence", []), state.get("knowledge_evidence", []))}


def score_confidence(state: ClinicalAgentState) -> ClinicalAgentState:
    return {**state, "confidence": ConfidenceScorer.score(state.get("patient_evidence", []), state.get("knowledge_evidence", []))}


def format_response(state: ClinicalAgentState) -> ClinicalAgentState:
    response = AnswerFormatter.format(
        question=state["question"],
        answer=state.get("safe_answer", state.get("raw_answer", "")),
        patient_evidence=state.get("patient_evidence", []),
        knowledge_evidence=state.get("knowledge_evidence", []),
        source_sections=state.get("source_sections", []),
        citations=state.get("citations", []),
        confidence=state.get("confidence", 0.0),
    )
    response["drug_interactions"] = state.get("drug_interactions", {})
    response["lab_analysis"] = state.get("lab_analysis", {})
    response["risk_assessment"] = state.get("risk_assessment", {})
    return {**state, "final_response": response}


def build_clinical_agent():
    graph = StateGraph(ClinicalAgentState)
    graph.add_node("retrieve_knowledge", retrieve_knowledge)
    graph.add_node("check_drug_interactions", check_drug_interactions)
    graph.add_node("analyze_labs", analyze_labs)
    graph.add_node("assess_risk", assess_risk)
    graph.add_node("build_patient_evidence", build_patient_evidence)
    graph.add_node("generate_answer", generate_answer)
    graph.add_node("apply_safety", apply_safety)
    graph.add_node("build_citations", build_citations)
    graph.add_node("score_confidence", score_confidence)
    graph.add_node("format_response", format_response)
    graph.set_entry_point("retrieve_knowledge")
    graph.add_edge("retrieve_knowledge", "check_drug_interactions")
    graph.add_edge("check_drug_interactions", "analyze_labs")
    graph.add_edge("analyze_labs", "assess_risk")
    graph.add_edge("assess_risk", "build_patient_evidence")
    graph.add_edge("build_patient_evidence", "generate_answer")
    graph.add_edge("generate_answer", "apply_safety")
    graph.add_edge("apply_safety", "build_citations")
    graph.add_edge("build_citations", "score_confidence")
    graph.add_edge("score_confidence", "format_response")
    graph.add_edge("format_response", END)
    return graph.compile()


class PatientAnswerWorkflow:
    _agent = None

    @classmethod
    def get_agent(cls):
        if cls._agent is None:
            cls._agent = build_clinical_agent()
        return cls._agent

    @staticmethod
    def run(question: str, patient_evidence: list, knowledge_evidence: list, source_sections: list,
            patient_context: str = "", patient: dict = None, labs: list = None, vitals: list = None, medications: list = None) -> dict:
        agent = PatientAnswerWorkflow.get_agent()
        initial_state = ClinicalAgentState(
            question=question, patient_context=patient_context,
            patient=patient or {}, labs=labs or [], vitals=vitals or [], medications=medications or [],
            patient_evidence=patient_evidence, knowledge_evidence=knowledge_evidence, source_sections=source_sections,
            drug_interactions={}, lab_analysis={}, risk_assessment={},
            raw_answer="", safe_answer="", citations=[], confidence=0.0, final_response={},
        )
        result = agent.invoke(initial_state)
        return result.get("final_response", {"answer": "Agent failed.", "citations": [], "confidence": 0.0})