from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ImageUpdate(BaseModel):
    url: str
    meta_data: dict

class ImageResponse(BaseModel):
    id: int
    url: str
    meta_data: dict
    created_at: datetime

    # tells Pydantic how to read SQLAlchemy objects directly
    model_config = ConfigDict(from_attributes=True)

class ImageList(BaseModel):
    images: list[dict] = []

    # tells Pydantic how to read SQLAlchemy objects directly
    model_config = ConfigDict(from_attributes=True)
