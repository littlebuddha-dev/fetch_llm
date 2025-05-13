# llm_api/providers/base.py
import abc

class LLMProvider(abc.ABC):
    def __init__(self, config: dict = {}):
        self.config = config

    @abc.abstractmethod
    async def call(self, prompt: str, system_prompt: str = "", **kwargs) -> dict:
        pass