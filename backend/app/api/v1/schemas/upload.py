from pydantic import BaseModel


class UploadResponse(BaseModel):
    message: str
    file_id: str
    filename: str
    content_type: str
    file_path: str
    file_size: int