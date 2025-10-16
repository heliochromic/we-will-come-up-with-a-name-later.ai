from pydantic import BaseModel, HttpUrl
from typing import Optional
from uuid import UUID
from datetime import datetime



class TranscriptBase(BaseModel):
    video_url: HttpUrl
    transcript_text: Optional[str] = None
    language: Optional[str] = None
    duration: Optional[float] = None



class TranscriptCreate(TranscriptBase):
    pass



class TranscriptResponse(TranscriptBase):
    transcript_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
