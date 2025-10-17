from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.user import GenderEnum


class UserBase(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None
    gender: Optional[GenderEnum] = None
    birth_date: Optional[datetime] = None


class UserCreate(UserBase):
    password: str



class UserResponse(UserBase):
    user_id: UUID
    is_admin: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
