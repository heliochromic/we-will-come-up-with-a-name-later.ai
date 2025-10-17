from sqlalchemy import Column, String, Text, DateTime, Float, JSON, func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.core.database import Base


class Transcript(Base):
    __tablename__ = "transcripts"

    transcript_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    video_url = Column(Text, nullable=False, unique=True, index=True)
    transcript_text = Column(Text, nullable=True)
    language = Column(String(50), nullable=True)
    duration = Column(Float, nullable=True)
    # metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return (
            f"<Transcript(transcript_id={self.transcript_id}, "
            f"video_url='{self.video_url}', language='{self.language}')>"
        )
