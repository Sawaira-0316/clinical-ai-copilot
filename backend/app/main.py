from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.db.session import engine, Base

# Import all models so SQLAlchemy registers them before create_all
from app.db.models import (  # noqa: F401
    patient,
    clinical_note,
    lab_result,
    vital_sign,
    medication,
    timeline_event,
    knowledge_document,
    knowledge_chunk,
)

from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all tables on startup if they don't exist
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables verified/created.")
    yield
    print("🛑 Shutting down Clinical AI Copilot backend.")


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Production-ready Clinical AI Copilot API",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS — allows Streamlit frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "app": settings.APP_NAME}