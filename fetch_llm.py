# /llm_api/fetch_llm.py

import argparse
import asyncio
import base64
import os
import json

from llm_api.providers import get_provider
from whisper import load_model as load_whisper_model  # openai-whisper を使用

def encode_image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def transcribe_audio(audio_path: str) -> str:
    model = load_whisper_model("base")
    result = model.transcribe(audio_path)
    return result["text"]

MODE_SYSTEM_PROMPTS = {
    "simple": "",
    "chat": "あなたは親切なチャット相手です。",
    "reasoning": "あなたは厳密に思考する論理的アシスタントです。思考を段階的に説明してください。",
    "qa": "あなたは質問に端的に答える優秀な知識アシスタントです。",
    "summary": "次のテキストを簡潔に要約してください。",
    "verify": "指示に従って、比較・検証・真偽を明確に答えてください。",
}

async def fetch_llm(provider_name: str, input_text: str, system_prompt: str = "", **kwargs) -> dict:
    provider = get_provider(provider_name)
    if not provider:
        raise ValueError(f"Unknown provider: {provider_name}")
    return await provider.call(input_text, system_prompt, **kwargs)

async def main():
    parser = argparse.ArgumentParser(description="LLM Unified CLI")
    parser.add_argument("provider", help="Provider name: ollama, openai, claude, gemini, huggingface")
    parser.add_argument("prompt", nargs="?", help="Prompt string (or use --input-file or --audio)")
    parser.add_argument("--input-file", help="File with one prompt per line")
    parser.add_argument("--image", help="Image file to include (base64-encoded)")
    parser.add_argument("--audio", help="Audio file to transcribe and use as prompt")
    parser.add_argument("--model", help="Model to use")
    parser.add_argument("--system", help="Custom system prompt (overrides mode)")
    parser.add_argument("--mode", choices=MODE_SYSTEM_PROMPTS.keys(), default="simple", help="Prompt purpose/mode")
    parser.add_argument("--json", action="store_true", help="Output full JSON response")
    args = parser.parse_args()

    prompts = []

    if args.audio:
        transcript = transcribe_audio(args.audio)
        prompts = [transcript]
    elif args.input_file:
        with open(args.input_file, "r", encoding="utf-8") as f:
            prompts = [line.strip() for line in f if line.strip()]
    elif args.prompt:
        prompts = [args.prompt]
    else:
        print("❌ エラー: prompt、--input-file、--audio のいずれかを指定してください。")
        return

    system_prompt = args.system or MODE_SYSTEM_PROMPTS[args.mode]
    image_base64 = encode_image_to_base64(args.image) if args.image else None

    for prompt in prompts:
        result = await fetch_llm(
            provider_name=args.provider,
            input_text=prompt,
            system_prompt=system_prompt,
            model=args.model,
            image_base64=image_base64
        )

        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print("🧠 PROMPT:", prompt)
            print("💬 RESPONSE:", result["text"])
            print("-" * 50)

if __name__ == "__main__":
    asyncio.run(main())
