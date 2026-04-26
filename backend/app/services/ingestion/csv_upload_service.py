from sqlalchemy.orm import Session
from app.services.ingestion.csv_parser import CSVParser
from app.services.clinical.patient_service import PatientService
from app.utils.file_helpers import ensure_upload_dir, generate_file_metadata, UPLOAD_DIR


class CSVUploadService:
    @staticmethod
    def process_patient_csv(content: bytes, db: Session = None, filename: str = "upload.csv") -> dict:
        # Parse based on file type
        patients, parse_errors = CSVParser.parse_patients_csv(content, filename=filename)

        # Save raw file
        ensure_upload_dir()
        file_id, safe_filename = generate_file_metadata(filename)
        file_path = UPLOAD_DIR / safe_filename
        file_path.write_bytes(content)

        # Insert to DB
        created = PatientService.create_patients_bulk(db, patients)

        return {
            "file_id": file_id,
            "filename": safe_filename,
            "file_size": len(content),
            "patients_parsed": len(patients),
            "patients_created": len(created),
            "skipped_rows": len(parse_errors),
            "parse_errors": parse_errors,
            "message": f"Successfully imported {len(created)} patients.",
        }