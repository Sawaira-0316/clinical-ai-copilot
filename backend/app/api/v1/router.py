from fastapi import APIRouter

from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.uploads import router as uploads_router
from app.api.v1.routes.patients import router as patients_router
from app.api.v1.routes.timeline import router as timeline_router
from app.api.v1.routes.clinical_notes import router as clinical_notes_router
from app.api.v1.routes.labs import router as labs_router
from app.api.v1.routes.vitals import router as vitals_router
from app.api.v1.routes.medications import router as medications_router
from app.api.v1.routes.patient_summary import router as patient_summary_router
from app.api.v1.routes.patient_alerts import router as patient_alerts_router
from app.api.v1.routes.patient_qa import router as patient_qa_router
from app.api.v1.routes.knowledge_base import router as knowledge_base_router
from app.api.v1.routes.knowledge_vector import router as knowledge_vector_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(uploads_router)
api_router.include_router(patients_router)
api_router.include_router(timeline_router)
api_router.include_router(clinical_notes_router)
api_router.include_router(labs_router)
api_router.include_router(vitals_router)
api_router.include_router(medications_router)
api_router.include_router(patient_summary_router)
api_router.include_router(patient_alerts_router)
api_router.include_router(patient_qa_router)
api_router.include_router(knowledge_base_router)
api_router.include_router(knowledge_vector_router)
