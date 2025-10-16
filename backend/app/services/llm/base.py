from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from enum import Enum


class LLMProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class LLMMessage:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content


class BaseLLM(ABC):
    def __init__(self, api_key: str, model: str, temperature: float = 0.7, max_tokens: int = 1000):
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    @abstractmethod
    async def generate(self, messages: List[LLMMessage], **kwargs) -> str:
        pass
