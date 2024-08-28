import asyncio
from util.llm import LLMProviders
import logging


# Panel of LLM Evaluators (PoLL)
# https://arxiv.org/abs/2306.05685v4
class PollAlgo:
    def __init__(self, models: list[str] = []):
        self.providers = llm_providers = LLMProviders()
        self.llm = llm_providers["ollama"]
        # Can customize your own PoLL
        self.models = models

    async def create_poll_completion(self, messages):
        try:
            results = await asyncio.gather(
                *(self._run_completion(messages, i) for i in range(len(self.models)))
            )
            return results
        except Exception as e:
            logging.error(f"Error in create_poll_completion: {e}")
            return []

    async def _run_completion(self, messages, model_id: int):
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, self._sync_run_completion, messages, model_id
            )
            return result
        except Exception as e:
            logging.error(f"Error in _run_completion: {e}")
            return None

    def _sync_run_completion(self, messages, model_id: int):
        try:
            llm = self.llm
            result = llm.chat.completions.create(
                messages=messages,
                model=self.models[model_id],
                temperature=0.8,
            )
            return result.choices[0].message.content
        except Exception as e:
            logging.error(f"Error in _sync_run_completion: {e}")
            return ""
