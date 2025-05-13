# llm_api/providers/huggingface.py
import os
import aiohttp
import base64
from .base import LLMProvider

class HuggingFaceProvider(LLMProvider):
    async def call(self, prompt: str, system_prompt: str = "", **kwargs) -> dict:
        model = kwargs.get("model", "Salesforce/blip-image-captioning-base")
        token = os.getenv("HF_TOKEN")
        url = f"https://api-inference.huggingface.co/models/{model}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        image_b64 = kwargs.get("image_base64")
        inputs = prompt
        if image_b64:
            inputs = f"data:image/jpeg;base64,{image_b64}"

        payload = {"inputs": inputs}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as res:
                data = await res.json()
                return {
                    "text": data[0].get("generated_text", "(no response)") if isinstance(data, list) else str(data),
                    "raw_response": data,
                    "usage": {}
                }
