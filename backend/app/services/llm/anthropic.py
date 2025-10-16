from typing import List
from app.services.llm.base import BaseLLM, LLMMessage as Message


class AnthropicLLM(BaseLLM):
    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022", **kwargs):
        super().__init__(api_key, model, **kwargs)
        from anthropic import AsyncAnthropic
        self.client = AsyncAnthropic(api_key=api_key)

    async def generate(self, messages: List[Message], **kwargs) -> str:
        system_message = None
        formatted_messages = []

        for msg in messages:
            if msg.role == "system":
                system_message = msg.content
            else:
                formatted_messages.append(
                    {"role": msg.role, "content": msg.content})

        response = await self.client.messages.create(
            model=self.model,
            system=system_message,
            messages=formatted_messages,
            temperature=kwargs.get("temperature", self.temperature),
            max_tokens=kwargs.get("max_tokens", self.max_tokens)
        )
        return response.content[0].text
