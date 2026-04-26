# AI Enginer Purpose

Handles all AI and ML processing for clinical data analysis, question answering, and insight generation.

## Responsibilities

- Document processing and embeddings
- Retrieval-augmented generation (RAG)
- Workflow orchestration
- Safety and quality checks

## Key Components

- `embeddings/`: Text embedding models
- `retrieval/`: Document search pipeline
- `vector_store/`: Qdrant integration
- `workflows/`: LangGraph workflow definitions
- `safety/`: Content filtering

## RAG Pipeline

Input Query → Retrieval → Re-ranking → Generation → Safety Check → Response

## Tech Stack

- LangChain/LangGraph
- Qdrant vector database
- OpenAI/Anthropic models
