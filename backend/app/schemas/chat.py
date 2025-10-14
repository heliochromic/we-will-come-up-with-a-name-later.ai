from pydantic import BaseModel
from typing import Optional


class ChatBase(BaseModel):
    pass


class ChatCreate(ChatBase):
    pass


class ChatResponse(ChatBase):
    pass


class LLMRequestSchema(BaseModel):
    pass


class LLMResponseSchema(BaseModel):
    pass
