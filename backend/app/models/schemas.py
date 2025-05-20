from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class SummaryRequest(BaseModel):
    filename: str
    content: str


class SummaryResponse(BaseModel):
    id: int
    filename: str
    content: str
    summary: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
