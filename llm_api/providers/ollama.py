# llm_api/providers/ollama.py
import aiohttp
import json
from .base import LLMProvider

class OllamaProvider(LLMProvider):
    async def call(self, prompt: str, system_prompt: str = "", **kwargs) -> dict:
        model = kwargs.get("model", "gemma3:latest")
        image_b64 = kwargs.get("image_base64")
        use_image = image_b64 is not None

        if use_image:
            url = "http://localhost:11434/api/generate"
            payload = {
                "model": model,
                "prompt": prompt,
                "images": [image_b64]
            }
        else:
            url = "http://localhost:11434/v1/chat/completions"
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "stream": False
            }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as res:
                if use_image:
                    text_data = await res.text()
                    lines = text_data.strip().splitlines()
                    json_objects = [json.loads(line) for line in lines if line.strip()]
                    final_text = "".join(obj.get("response", "") for obj in json_objects)
                    return {
                        "text": final_text,
                        "raw_response": json_objects,
                        "usage": {}
                    }
                else:
                    data = await res.json()
                    return {
                        "text": data.get("choices", [{}])[0].get("message", {}).get("content", "(no response)"),
                        "raw_response": data,
                        "usage": data.get("usage", {})
                    }
