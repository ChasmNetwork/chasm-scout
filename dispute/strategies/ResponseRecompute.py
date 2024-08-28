from util.chasm import Message
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import asyncio
from typing import List, Tuple
from util.llm import LLMProviders


class ResponseRecomputeAnalysis:
    def __init__(self, model: str):
        self.model = model
        self.llm_providers = LLMProviders()

    async def analyse(
        self,
        input: List[Message],
        output: str,
        seed: int,
        provider: str = "ollama",
    ) -> Tuple[float, str]:
        loop = asyncio.get_event_loop()
        score, output = await loop.run_in_executor(
            None, self._sync_analyse, input, output, seed, provider
        )
        return score, output

    def _sync_analyse(
        self,
        input: List[Message],
        output: str,
        seed: int,
        provider: str,
    ) -> Tuple[float, str]:
        llm = self.llm_providers[provider]
        recompute_output = llm.chat.completions.create(
            messages=input,
            model=self.model,
            temperature=0,
            seed=seed,
        )
        output_response = recompute_output.choices[0].message.content
        assert output_response is not None, "Recompute output is None"
        assert isinstance(output_response, str), "Recompute output is not a string"
        score = self.similarity(output_response, output)
        return score, output_response

    def similarity(self, text1: str, text2: str) -> float:
        vectorizer = TfidfVectorizer().fit_transform([text1, text2])
        vectors = vectorizer.toarray()
        cosine_sim = cosine_similarity(vectors[0:1], vectors[1:])
        score = cosine_sim[0][0]
        return 1 - score
