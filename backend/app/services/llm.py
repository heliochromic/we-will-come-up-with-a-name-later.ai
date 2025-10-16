from typing import Optional, List, Dict
from app.services.llm.base import BaseLLM, LLMProvider, LLMMessage as Message
from app.services.llm.openai import OpenAILLM
from app.services.llm.anthropic import AnthropicLLM


class LLMFactory:
    @staticmethod
    def create_llm(provider: LLMProvider, api_key: str, model: Optional[str] = None, **kwargs) -> BaseLLM:
        if provider == LLMProvider.OPENAI:
            return OpenAILLM(api_key, model or "gpt-4", **kwargs)
        elif provider == LLMProvider.ANTHROPIC:
            return AnthropicLLM(api_key, model or "claude-3-5-sonnet-20241022", **kwargs)
        else:
            raise ValueError(f"Unsupported provider: {provider}")


class LLMService:
    def __init__(self, provider: LLMProvider, api_key: str, model: Optional[str] = None, **kwargs):
        self.llm = LLMFactory.create_llm(provider, api_key, model, **kwargs)

    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        msg_objects = [Message(msg["role"], msg["content"])
                       for msg in messages]
        return await self.llm.generate(msg_objects, **kwargs)
