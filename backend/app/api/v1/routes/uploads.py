from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.ingestion.csv_upload_service import CSVUploadService
from app.api.v1.schemas.upload_response import CSVUploadResponse

router = APIRouter(prefix="/uploads", tags=["Uploads"])

ALLOWED_EXTENSIONS = {"csv", "xlsx", "xls", "pdf", "txt"}


@router.post("/patients/csv", response_model=CSVUploadResponse)
async def upload_patients_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Upload patient data file.
    Supports: CSV, Excel (.xlsx/.xls), PDF, TXT
    """
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    ext = file.filename.lower().split(".")[-1] if "." in file.filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type '.{ext}' not supported. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    content = await file.read()

    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    if len(content) > 50 * 1024 * 1024:  # 50 MB limit
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 50 MB.")

    try:
        result = CSVUploadService.process_patient_csv(
    content=content,
    filename=file.filename,
    db=db
)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

    return result
