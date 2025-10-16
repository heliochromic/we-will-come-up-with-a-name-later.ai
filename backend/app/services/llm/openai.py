from typing import List
from app.services.llm.base import BaseLLM, LLMMessage as Message


class OpenAILLM(BaseLLM):
    def __init__(self, api_key: str, model: str = "gpt-4", **kwargs):
        super().__init__(api_key, model, **kwargs)
        from openai import AsyncOpenAI
        self.client = AsyncOpenAI(api_key=api_key)

    async def generate(self, messages: List[Message], **kwargs) -> str:
        formatted_messages = [
            {"role": msg.role, "content": msg.content} for msg in messages]

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=formatted_messages,
            temperature=kwargs.get("temperature", self.temperature),
            max_tokens=kwargs.get("max_tokens", self.max_tokens)
        )
        return response.choices[0].message.content
