from enum import Enum
from openai import OpenAI
from config import GROQ_API_KEY, LLM_API_KEY, LLM_BASE_URL, OPENROUTER_API_KEY


class LLMProvider(Enum):
    OLLAMA = "ollama"
    GROQ = "groq"
    OPENROUTER = "openrouter"
    OPENAI = "openai"


AI_MODEL_MAP = {
    "gemma2-9b-it": {
        LLMProvider.GROQ: "gemma2-9b-it",
        LLMProvider.OPENROUTER: "google/gemma-2-9b-it",
        LLMProvider.OLLAMA: "gemma2:9b",
    },
    "gemma-7b-it": {
        LLMProvider.GROQ: "gemma-7b-it",
        LLMProvider.OPENROUTER: "google/gemma-7b-it",
        LLMProvider.OLLAMA: "gemma:7b",
    },
    "gpt-3.5-turbo-0125": {
        LLMProvider.OPENAI: "gpt-3.5-turbo-0125",
    },
    "gpt-3.5-turbo": {
        LLMProvider.OPENAI: "gpt-3.5-turbo-0125",
    },
    "gpt-4-turbo": {
        LLMProvider.OPENAI: "gpt-4-turbo-2024-04-09",
    },
    "gpt-4-turbo-2024-04-09": {
        LLMProvider.OPENAI: "gpt-4-turbo-2024-04-09",
    },
    "gpt-4": {
        LLMProvider.OPENAI: "gpt-4-0613",
    },
    "gpt-4-0613": {
        LLMProvider.OPENAI: "gpt-4-0613",
    },
}


class LLMProviders:
    def __init__(self):
        self.supportedModels = AI_MODEL_MAP.keys()
        self.supportedProviders = [provider for provider in LLMProvider]

    def __getitem__(self, provider: str):
        if provider == "groq":
            return self.groq()
        if provider == "openrouter":
            return self.openrouter()
        if provider == "ollama":
            return self.ollama()
        raise Exception("LLM provider is not supported")

    def groq(self):
        assert GROQ_API_KEY is not None, "GROQ_API_KEY is not set"
        return OpenAI(base_url="https://api.groq.com/openai/v1/", api_key=GROQ_API_KEY)

    def openrouter(self):
        assert OPENROUTER_API_KEY is not None, "OPENROUTER_API_KEY is not set"
        return OpenAI(
            base_url="https://api.openrouter.io/openai/v1/", api_key=OPENROUTER_API_KEY
        )

    def ollama(self):
        assert LLM_BASE_URL is not None, "LLM_BASE_URL is not set"
        return OpenAI(base_url=LLM_BASE_URL, api_key=LLM_API_KEY)
