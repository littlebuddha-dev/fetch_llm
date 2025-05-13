# llm_api/providers/claude.py
import os
import aiohttp
from .base import LLMProvider

class ClaudeProvider(LLMProvider):
    async def call(self, prompt: str, system_prompt: str = "", **kwargs) -> dict:
        model = kwargs.get("model", "claude-3-opus-20240229")
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": os.getenv("CLAUDE_API_KEY"),
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }

        image_b64 = kwargs.get("image_base64")
        content = [
            {"type": "text", "text": prompt}
        ]
        if image_b64:
            content.append({"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": image_b64}})

        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": content}
            ],
            "system": system_prompt,
            "max_tokens": kwargs.get("max_tokens", 1024)
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as res:
                data = await res.json()
                return {
                    "text": data.get("content", "(no response)"),
                    "raw_response": data,
                    "usage": {}
                }