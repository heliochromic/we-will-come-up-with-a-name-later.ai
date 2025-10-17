from typing import List, Dict
from openai import OpenAI
from anthropic import Anthropic
from app.core.config import settings


class LLMService:
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None

        if settings.OPENAI_API_KEY:
            self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

        if settings.ANTHROPIC_API_KEY:
            self.anthropic_client = Anthropic(
                api_key=settings.ANTHROPIC_API_KEY)

    def generate_response(
        self,
        provider: str,
        messages: List[Dict[str, str]],
        temperature: float = None,
        max_tokens: int = None
    ) -> str:
        temperature = temperature or settings.LLM_TEMPERATURE
        max_tokens = max_tokens or settings.LLM_MAX_TOKENS

        if provider == "openai":
            return self._generate_openai_response(messages, temperature, max_tokens)
        elif provider == "claude":
            return self._generate_claude_response(messages, temperature, max_tokens)
        else:
            raise ValueError(f"Invalid provider: {provider}")

    def _generate_openai_response(
        self,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: int
    ) -> str:
        if not self.openai_client:
            raise ValueError("OpenAI API key not configured")

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            raise ValueError(f"OpenAI API error: {str(e)}")

    def _generate_claude_response(
        self,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: int
    ) -> str:
        if not self.anthropic_client:
            raise ValueError("Anthropic API key not configured")

        try:
            system_message = None
            claude_messages = []

            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    claude_messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })

            request_params = {
                "model": "claude-3-5-sonnet-20241022",
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": claude_messages
            }

            if system_message:
                request_params["system"] = system_message

            response = self.anthropic_client.messages.create(**request_params)

            return response.content[0].text
        except Exception as e:
            raise ValueError(f"Anthropic API error: {str(e)}")

    def format_chat_history(
        self,
        chat_messages: List,
        new_user_message: str,
        system_prompt: str = None
    ) -> List[Dict[str, str]]:
        messages = []

        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })

        for msg in chat_messages:
            role = "assistant" if msg.sender == "llm" else "user"
            messages.append({
                "role": role,
                "content": msg.message_text
            })

        messages.append({
            "role": "user",
            "content": new_user_message
        })

        return messages


llm_service = LLMService()
