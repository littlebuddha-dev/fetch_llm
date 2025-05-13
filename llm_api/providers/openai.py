# llm_api/providers/openai.py
import os
import aiohttp
from .base import LLMProvider

class OpenAIProvider(LLMProvider):
    async def call(self, prompt: str, system_prompt: str = "", **kwargs) -> dict:
        model = kwargs.get("model", "gpt-4-vision-preview")
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
            "Content-Type": "application/json"
        }

        image_b64 = kwargs.get("image_base64")
        if image_b64:
            content = [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
            ]
            messages = [{"role": "user", "content": content}]
        else:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]

        payload = {
            "model": model,
            "messages": messages,
            "stream": False
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as res:
                data = await res.json()
                return {
                    "text": data.get("choices", [{}])[0].get("message", {}).get("content", "(no response)"),
                    "raw_response": data,
                    "usage": data.get("usage", {})
                }