from pydantic import BaseModel
from typing import Optional


class TranscriptBase(BaseModel):
    pass


class TranscriptCreate(TranscriptBase):
    pass


class TranscriptResponse(TranscriptBase):
    pass
