# llm_api/providers/gemini.py
import os
import aiohttp
from .base import LLMProvider

class GeminiProvider(LLMProvider):
    async def call(self, prompt: str, system_prompt: str = "", **kwargs) -> dict:
        api_key = os.getenv("GEMINI_API_KEY")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent?key={api_key}"

        image_b64 = kwargs.get("image_base64")
        parts = [{"text": prompt}]
        if image_b64:
            parts.append({"inline_data": {"mime_type": "image/jpeg", "data": image_b64}})

        payload = {
            "contents": [
                {"role": "user", "parts": parts}
            ]
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as res:
                data = await res.json()
                candidates = data.get("candidates", [])
                return {
                    "text": candidates[0]["content"]["parts"][0]["text"] if candidates else "(no response)",
                    "raw_response": data,
                    "usage": {}
                }
