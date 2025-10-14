from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    pass
