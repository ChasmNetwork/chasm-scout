from openai import OpenAI

from config import LLM_API_KEY, LLM_BASE_URL

# Using ollama
llm = OpenAI(
    base_url=LLM_BASE_URL,
    api_key=LLM_API_KEY
)