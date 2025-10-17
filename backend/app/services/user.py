from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.services.base import BaseService
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.schemas.user import UserCreate


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService(BaseService[User, UserRepository]):
    def __init__(self):
        super().__init__(UserRepository, User)

    def _validate_create(self, obj: User) -> None:
        if not obj.name or len(obj.name.strip()) == 0:
            raise ValueError("User name cannot be empty")

        if not obj.email or len(obj.email.strip()) == 0:
            raise ValueError("User email cannot be empty")

        if obj.age is not None and obj.age < 0:
            raise ValueError("User age cannot be negative")

    def _validate_update(self, obj: User, update_data: Dict[str, Any]) -> None:
        if "name" in update_data and (not update_data["name"] or len(update_data["name"].strip()) == 0):
            raise ValueError("User name cannot be empty")

        if "email" in update_data and (not update_data["email"] or len(update_data["email"].strip()) == 0):
            raise ValueError("User email cannot be empty")

        if "age" in update_data and update_data["age"] is not None and update_data["age"] < 0:
            raise ValueError("User age cannot be negative")

    def _validate_delete(self, obj: User) -> None:
        pass

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        repo = self._get_repository(db)
        return repo.get_by_email(email)

    def create_user(self, db: Session, user_data: UserCreate) -> User:
        existing_user = self.get_by_email(db, user_data.email)
        if existing_user:
            raise ValueError(
                f"User with email {user_data.email} already exists")

        hashed_password = self._hash_password(user_data.password)

        user = User(
            name=user_data.name,
            email=user_data.email,
            hashed_password=hashed_password,
            age=user_data.age,
            gender=user_data.gender,
            birth_date=user_data.birth_date,
        )

        return self.create(db, user)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def _hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def authenticate_user(self, db: Session, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email)
        if not user:
            return None

        if not self.verify_password(password, user.hashed_password):
            return None

        return user

    def update_user_profile(self, db: Session, user_id: int, **kwargs) -> Optional[User]:
        if "password" in kwargs:
            plain_password = kwargs.pop("password")
            kwargs["hashed_password"] = self._hash_password(plain_password)

        return self.update(db, user_id, **kwargs)

    def user_exists(self, db: Session, email: str) -> bool:
        return self.get_by_email(db, email) is not None


user_service = UserService()
