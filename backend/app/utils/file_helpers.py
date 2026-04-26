import uuid
from pathlib import Path

UPLOAD_DIR = Path("uploads")
ALLOWED_EXTENSIONS = {".csv"}


def ensure_upload_dir() -> None:
    """Create uploads/ directory if it doesn't exist."""
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def validate_file_extension(filename: str) -> str:
    """
    Validate the file has an allowed extension.
    Returns the extension (e.g. '.csv') or raises ValueError.
    """
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"File type '{ext}' is not supported. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    return ext


def generate_file_metadata(original_filename: str) -> tuple[str, str]:
    """
    Generate a unique file ID and safe filename.
    Returns: (file_id, safe_filename)
    Example: ('a1b2c3', 'a1b2c3_patients.csv')
    """
    file_id = str(uuid.uuid4())
    ext = Path(original_filename).suffix.lower()
    safe_filename = f"{file_id}_{original_filename}"
    return file_id, safe_filename