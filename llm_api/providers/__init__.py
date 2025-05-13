from .ollama import OllamaProvider
from .openai import OpenAIProvider
from .claude import ClaudeProvider
from .gemini import GeminiProvider
from .huggingface import HuggingFaceProvider

def get_provider(name: str):
    name = name.lower()
    if name == "ollama":
        return OllamaProvider()
    elif name == "openai":
        return OpenAIProvider()
    elif name == "claude":
        return ClaudeProvider()
    elif name == "gemini":
        return GeminiProvider()
    elif name == "huggingface":
        return HuggingFaceProvider()
    else:
        raise ValueError(f"Unknown provider: {name}")