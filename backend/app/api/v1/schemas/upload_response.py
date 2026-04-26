from pydantic import BaseModel
from typing import List


class CSVUploadResponse(BaseModel):
    file_id: str
    filename: str
    file_size: int
    patients_parsed: int
    patients_created: int
    skipped_rows: int
    parse_errors: List[str]
    message: str