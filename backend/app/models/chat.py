from sqlalchemy import Column, DateTime, ForeignKey, func, String, Text, Float, Integer, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class Chat(Base):
    __tablename__ = "chats"

    chat_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    transcript_id = Column(UUID(as_uuid=True), ForeignKey("transcripts.transcript_id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")
    transcript = relationship("Transcript", backref="chats")

    def __repr__(self):
        return f"<Chat(chat_id={self.chat_id}, transcript_id={self.transcript_id})>"



class Message(Base):
    __tablename__ = "messages"

    message_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    chat_id = Column(UUID(as_uuid=True), ForeignKey("chats.chat_id", ondelete="CASCADE"), nullable=False)
    sender = Column(String(50), nullable=False)
    message_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    chat = relationship("Chat", back_populates="messages")

    __table_args__ = (
        CheckConstraint("sender IN ('user', 'system', 'llm')", name="check_sender_valid"),
    )

    def __repr__(self):
        return f"<Message(chat_id={self.chat_id}, sender='{self.sender}', created_at={self.created_at})>"