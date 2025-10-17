from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime


class MessageBase(BaseModel):
    sender: str
    message_text: str


class MessageCreate(MessageBase):
    chat_id: UUID


class MessageResponse(MessageBase):
    message_id: UUID
    chat_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChatBase(BaseModel):
    transcript_id: Optional[UUID] = None


class ChatCreate(ChatBase):
    pass  # всі поля вже у базовій схемі


class ChatResponse(ChatBase):
    chat_id: UUID
    created_at: datetime
    messages: list[MessageResponse] = []

    model_config = ConfigDict(from_attributes=True)

class LLMRequestSchema(BaseModel):
    chat_id: UUID
    user_message: str


class LLMResponseSchema(BaseModel):
    chat_id: UUID
    llm_message: str
