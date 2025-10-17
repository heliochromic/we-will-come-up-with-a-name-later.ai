from pydantic import BaseModel, HttpUrl, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)
