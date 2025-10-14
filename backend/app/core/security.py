from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"])


def hash_password(password: str) -> str:
    pass


def verify_password(plain: str, hashed: str) -> bool:
    pass


def create_access_token(data: dict) -> str:
    pass


def decode_token(token: str) -> dict:
    pass
