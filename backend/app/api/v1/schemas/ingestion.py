from pydantic import BaseModel


class IngestionResponse(BaseModel):
    message: str
    file_id: str
    filename: str
    file_path: str
    file_size: int
    patients_created: int