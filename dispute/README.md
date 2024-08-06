## Ollama

```
LLM_BASE_URL=http://host.docker.internal:11434/v1
LLM_API_KEY=ollama
MODELS=llama3.1:8b,qwen:4b,mistral:7b
SIMULATION_MODEL=llama3.1:8b
ORCHESTRATOR_URL=https://orchestrator.chasm.net
WEBHOOK_API_KEY=
MIN_CONFIDENCE_SCORE=0.5
```

## OpenRouter

https://openrouter.ai/docs#models

```
LLM_API_KEY=
LLM_BASE_URL=https://openrouter.ai/api/v1
MODELS=google/gemma-7b-it,meta-llama/llama-3-8b-instruct,microsoft/wizardlm-2-7b,mistralai/mistral-7b-instruct-v0.3
SIMULATION_MODEL=meta-llama/llama-3-8b-instruct
```

## Groq

```
LLM_API_KEY=
LLM_BASE_URL=https://api.groq.com/openai/v1
MODELS=llama3-8b-8192,mixtral-8x7b-32768,gemma-7b-it
SIMULATION_MODEL=llama3-8b-8192
```
