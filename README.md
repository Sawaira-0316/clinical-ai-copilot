# 🏥 Clinical AI Copilot

> A production-ready, agentic AI assistant for clinical workflows  helping doctors review patient data faster, generate evidence-based insights, and make better decisions with AI support.


## 📌 Features

| Feature                               | Status |
| ------------------------------------- | ------ |
| Multi-format Upload (CSV, Excel, TXT) | ✅     |
| FastAPI Backend + SQLite              | ✅     |
| Patient List, Search, Detail          | ✅     |
| AI Clinical Summary (Groq LLaMA 3.3)  | ✅     |
| LangGraph Agentic Workflow (10 steps) | ✅     |
| RAG Pipeline + Qdrant Vector Search   | ✅     |
| Drug Interaction Checker              | ✅     |
| Lab Trend Analyzer                    | ✅     |
| Risk Scoring Engine                   | ✅     |
| Knowledge Base (Upload + Search)      | ✅     |
| Safety Guard + Confidence Scoring     | ✅     |
| Streamlit Cloud + Render Deployment   | ✅     |

---

## 🤖 LangGraph Agent — 10 Step Workflow

```
Doctor asks question
        ↓
Step 1:  Search medical guidelines (RAG + Qdrant)
Step 2:  Check drug interactions
Step 3:  Analyze lab trends + abnormalities
Step 4:  Calculate patient risk score
Step 5:  Build comprehensive patient evidence
Step 6:  Generate grounded answer (Groq LLaMA 3.3 70B)
Step 7:  Apply safety guard + disclaimers
Step 8:  Build evidence citations
Step 9:  Score answer confidence (0-100%)
Step 10: Format structured clinical response
        ↓
Doctor reviews answer with confidence score + sources
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         Streamlit Frontend               │
│      (Streamlit Cloud)                   │
└──────────────┬──────────────────────────┘
               │ HTTP REST API
┌──────────────▼──────────────────────────┐
│           FastAPI Backend                │
│              (Render)                    │
└──────────────┬──────────────────────────┘
               │
       ┌───────┴────────┐
       │                │
┌──────▼──────┐  ┌──────▼──────────────────┐
│   SQLite    │  │    LangGraph Agent        │
│  Database   │  │  10-step workflow         │
└─────────────┘  └──────────┬───────────────┘
                            │
            ┌───────────────┼──────────────┐
 ┌──────────▼──────┐  ┌─────▼──────┐  ┌───▼───────┐
 │    Qdrant       │  │  Groq API  │  │  SQLite   │
 │ Vector Database │  │ LLaMA 3.3  │  │ Patient   │
 └─────────────────┘  └────────────┘  └───────────┘
```

---

## 🛠️ Tech Stack

| Layer           | Technology             |
| --------------- | ---------------------- |
| Frontend        | Streamlit              |
| Backend         | FastAPI + Python 3.11  |
| Database        | SQLite                 |
| AI Model        | LLaMA 3.3 70B via Groq |
| AI Framework    | LangChain + LangGraph  |
| Vector DB       | Qdrant                 |
| Embeddings      | sentence-transformers  |
| Frontend Deploy | Streamlit Cloud        |
| Backend Deploy  | Render                 |

---

ScreenShots

## 🏠 Home
![Home](https://raw.githubusercontent.com/Sawaira-0316/clinical-ai-copilot/main/home.png)

---

## 🧠 Knowledge Base Detail
![Knowledge Base Detail](https://raw.githubusercontent.com/Sawaira-0316/clinical-ai-copilot/692636d8fb97257088995da0bfda705125d3a390/knowledge_base%20detail.png)

---

## 📚 Knowledge Base
![Knowledge Base](https://raw.githubusercontent.com/Sawaira-0316/clinical-ai-copilot/692636d8fb97257088995da0bfda705125d3a390/knowledge_base.png)

---

## 📋 Patient Details
![Patient Details](https://raw.githubusercontent.com/Sawaira-0316/clinical-ai-copilot/692636d8fb97257088995da0bfda705125d3a390/patients%20details.png)

---

## 🧑‍⚕️ Patients
![Patients](https://raw.githubusercontent.com/Sawaira-0316/clinical-ai-copilot/692636d8fb97257088995da0bfda705125d3a390/patients.png)


---


## 🚀 Live Demo

| Service          | URL                                                                          |
| ---------------- | ---------------------------------------------------------------------------- |
| 🎨 Frontend      |  |
| ⚙️ Backend API |    |
| 📖 Swagger Docs  | 

## ⚠️ Disclaimer

Clinical AI Copilot is for  **clinical workflow assistance only** . Not a replacement for professional medical judgment. All AI outputs must be reviewed by licensed clinicians before any clinical action is taken.
