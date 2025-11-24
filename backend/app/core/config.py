from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from pydantic import Field
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    APP_NAME: str = "YouTube LLM Agent API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Database settings - using Field with alias to map env var names
    DB_USER: str = Field(default="postgres", alias="user")
    DB_PASSWORD: str = Field(default="password", alias="password")
    DB_HOST: str = Field(default="localhost", alias="host")
    DB_PORT: str = Field(default="5432", alias="port")
    DB_NAME: str = Field(default="youtube_llm_db", alias="dbname")

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    SECRET_KEY: str = Field(default="your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)

    OPENAI_API_KEY: Optional[str] = Field(default=None)
    ANTHROPIC_API_KEY: Optional[str] = Field(default=None)

    CORS_ORIGINS: list = ["*"]

    DEFAULT_LLM_MODEL: str = Field(default="gpt-4.1")
    LLM_TEMPERATURE: float = Field(default=0.7)
    LLM_MAX_TOKENS: int = Field(default=2000)

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        populate_by_name=True  # This allows both the field name and alias to be used
    )


settings = Settings()
