import os
from dotenv import load_dotenv

load_dotenv()

LLM_BASE_URL = os.getenv("LLM_BASE_URL")
LLM_API_KEY = os.getenv("LLM_API_KEY")
MODELS = os.getenv("MODELS", "gemma2-9b-it").split(",")
SIMULATION_MODEL = os.getenv("SIMULATION_MODEL", "gemma2-9b-it")
ORCHESTRATOR_URL = os.getenv("ORCHESTRATOR_URL")
WEBHOOK_API_KEY = os.getenv("WEBHOOK_API_KEY")
MIN_CONFIDENCE_SCORE = float(os.getenv("MIN_CONFIDENCE_SCORE", 0.5))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

print(f"LOG_LEVEL: {LOG_LEVEL}")
print(f"MIN_CONFIDENCE_SCORE: {MIN_CONFIDENCE_SCORE}")
print(f"LLM_BASE_URL: {LLM_BASE_URL}")
print(f"MODELS: {MODELS}")
print(f"SIMULATION_MODEL: {SIMULATION_MODEL}")
print(f"ORCHESTRATOR_URL: {ORCHESTRATOR_URL}")
