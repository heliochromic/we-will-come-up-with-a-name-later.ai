from sqlalchemy import Column, String, DateTime, Boolean, Integer, func, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum

from app.core.database import Base


class GenderEnum(str, enum.Enum):
    male = "male"
    female = "female"
    other = "other"


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    age = Column(Integer)
    gender = Column(Enum(GenderEnum, name="gender_enum"), nullable=True)
    birth_date = Column(DateTime, nullable=True)

    is_admin = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return (
            f"<User(user_id={self.user_id}, name='{self.name}', email='{self.email}', "
            f"is_admin={self.is_admin})>"
        )
