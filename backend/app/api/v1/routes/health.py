from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "message": "Clinical AI Copilot backend is running"
    }