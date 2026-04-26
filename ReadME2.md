# 🏥 Clinical AI Copilot

> A production-ready, agentic AI assistant for clinical workflows — helping doctors review patient data faster, generate evidence-based insights, and make better decisions with AI support.

---

## 🚀 Live Demo

> Coming soon after deployment

---

## 📌 Project Status

| Phase    | Feature                     | Status         |
| -------- | --------------------------- | -------------- |
| Phase 1  | Data Ingestion (CSV upload) | ✅ Complete    |
| Phase 2  | Service Layer + DB          | ✅ Complete    |
| Phase 3  | AI Summary + Q&A            | ✅ Complete    |
| Phase 4  | RAG + Qdrant Vector Search  | 🔄 In Progress |
| Phase 5  | LangGraph Agentic Workflow  | 🔄 In Progress |
| Phase 6  | LangSmith Monitoring        | ⏳ Planned     |
| Phase 7  | Authentication + Login      | ⏳ Planned     |
| Phase 8  | Drug Interaction Checker    | ⏳ Planned     |
| Phase 9  | Risk Scoring Dashboard      | ⏳ Planned     |
| Phase 10 | Docker + Cloud Deployment   | ⏳ Planned     |

---

## ✅ What Works Right Now

* **CSV Patient Upload** — Upload any CSV format, auto-detects columns
* **Patient List + Search** — Search patients by name, view all records
* **Patient Detail Page** — Full patient overview with metrics
* **AI Summary** — Auto-generated clinical summary using LLaMA 3.3 via Groq
* **AI Q&A** — Ask clinical questions, get grounded answers
* **Timeline** — Chronological patient event history
* **Labs, Vitals, Medications** — Structured clinical data display
* **Alerts** — Automated abnormal value detection
* **FastAPI Backend** — Full REST API with Swagger docs
* **Streamlit Dashboard** — Premium dark UI

---

## 🤖 What We Are Building Next

### LangGraph Agentic Workflow

Instead of a simple AI call, the system will use a  **multi-step reasoning agent** :

```
Doctor asks question
        ↓
LangGraph Agent thinks: "What do I need?"
        ↓
Tool 1: Search patient DB (real data)
Tool 2: Search Qdrant (medical guidelines RAG)
Tool 3: Analyze lab trends
Tool 4: Check drug interactions
        ↓
Agent reasons over all findings
        ↓
Structured clinical answer with sources + confidence
        ↓
Doctor reviews and approves (Human-in-the-loop)
```

### RAG Pipeline with Qdrant

* Upload clinical guidelines, research papers, protocols
* Chunk and embed documents
* Store vectors in Qdrant
* Retrieve relevant context for every question

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│           Streamlit Frontend             │
│    (Patient Dashboard + AI Interface)    │
└──────────────┬──────────────────────────┘
               │ HTTP
┌──────────────▼──────────────────────────┐
│           FastAPI Backend                │
│         REST API + Swagger              │
└──────────────┬──────────────────────────┘
               │
       ┌───────┴────────┐
       │                │
┌──────▼──────┐  ┌──────▼──────────────────┐
│   SQLite    │  │    LangGraph Agent       │
│  (dev DB)   │  │  ┌─────────────────┐    │
│  PostgreSQL │  │  │ RAG Tool        │    │
│  (prod DB)  │  │  │ Patient Tool    │    │
└─────────────┘  │  │ Lab Analyzer    │    │
                 │  │ Drug Checker    │    │
                 │  └────────┬────────┘    │
                 └───────────┼─────────────┘
                             │
                 ┌───────────▼─────────────┐
                 │       Qdrant            │
                 │   Vector Database       │
                 │  (Medical Guidelines)   │
                 └─────────────────────────┘
                             │
                 ┌───────────▼─────────────┐
                 │    Groq API             │
                 │  LLaMA 3.3 70B          │
                 │  (Fast Inference)       │
                 └─────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer        | Technology                       |
| ------------ | -------------------------------- |
| Frontend     | Streamlit                        |
| Backend      | FastAPI + Python                 |
| Database     | SQLite (dev) / PostgreSQL (prod) |
| AI Model     | LLaMA 3.3 70B via Groq           |
| AI Framework | LangChain + LangGraph            |
| Vector DB    | Qdrant                           |
| Monitoring   | LangSmith                        |
| Embeddings   | sentence-transformers            |
| Deployment   | Docker + Railway/Render          |

---

## 📁 Project Structure

```
Clinical AI Copilot/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/v1/routes/     # API endpoints
│   │   ├── services/          # Business logic
│   │   │   ├── clinical/      # Patient, Summary, QA, Alerts
│   │   │   ├── ingestion/     # CSV parser, upload
│   │   │   ├── knowledge/     # RAG, Qdrant
│   │   │   └── agents/        # LangGraph workflows
│   │   ├── db/                # Models + Repositories
│   │   └── core/              # Config, settings
├── frontend_streamlit/         # Streamlit dashboard
│   ├── pages/                 # Multi-page app
│   ├── components/            # Reusable UI components
│   ├── services/              # API client services
│   └── styles/                # CSS styling
├── ai_engine/                 # AI components
│   ├── workflows/             # LangGraph workflows
│   ├── prompts/               # Prompt templates
│   └── tools/                 # Agent tools
└── infrastructure/            # Docker + deployment
```

---

## 🚀 Getting Started

### Prerequisites

* Python 3.11+
* Docker (for Qdrant)
* Groq API key (free at console.groq.com)

### Installation

```bash
# Clone the repository
git clone https://github.com/Sawaira-0316/clinical-ai-copilot.git
cd clinical-ai-copilot

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Start Qdrant
docker run -d -p 6333:6333 --name qdrant qdrant/qdrant

# Start backend
cd backend
uvicorn app.main:app --port 8001

# Start frontend (new terminal)
cd frontend_streamlit
streamlit run app.py
```

### Environment Variables

Create `backend/.env`:

```
APP_NAME=Clinical AI Copilot
API_V1_PREFIX=/api/v1
DEBUG=True
DATABASE_URL=sqlite:///./clinical_ai.db
GROQ_API_KEY=your_groq_key_here
QDRANT_HOST=localhost
QDRANT_PORT=6333
```

---

## 📊 API Endpoints

| Method | Endpoint                         | Description        |
| ------ | -------------------------------- | ------------------ |
| GET    | /api/v1/health                   | Health check       |
| POST   | /api/v1/uploads/patients/csv     | Upload patient CSV |
| GET    | /api/v1/patients                 | Get all patients   |
| GET    | /api/v1/patients/{id}            | Get patient by ID  |
| GET    | /api/v1/patients/{id}/summary    | AI summary         |
| GET    | /api/v1/patients/{id}/alerts     | Patient alerts     |
| POST   | /api/v1/qa/ask                   | Ask AI question    |
| GET    | /api/v1/timeline/{id}            | Patient timeline   |
| GET    | /api/v1/labs/patient/{id}        | Lab results        |
| GET    | /api/v1/vitals/patient/{id}      | Vital signs        |
| GET    | /api/v1/medications/patient/{id} | Medications        |

---

## ⚠️ Disclaimer

Clinical AI Copilot is designed for clinical workflow assistance only. It is not a replacement for professional medical judgment or FDA-approved diagnostic tools. Always consult qualified healthcare professionals for medical decisions. All AI outputs must be reviewed and validated by licensed clinicians before any clinical action is taken.

---

## 👨‍💻 Developer

**Sawaira Asghar**
AI Engineer | LangChain | LangGraph | RAG | FastAPI | Streamlit

---

## 📄 License

MIT License — see LICENSE file for details.
