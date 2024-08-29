from util.chasm import Message
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import asyncio
from typing import List, Tuple
from util.llm import LLMProviders


class ResponseSimilarityAnalysis:
    def __init__(self, model: str):
        self.model = model
        self.provider = LLMProviders()

    async def analyze(self, input: List[Message], output: str) -> Tuple[float, str]:
        loop = asyncio.get_event_loop()
        score, output = await loop.run_in_executor(
            None, self._sync_analyse, input, output
        )
        return score, output

    def _sync_analyse(self, input: List[Message], output: str):
        llm = self.provider["ollama"]
        simulated_output = llm.chat.completions.create(
            messages=input,
            model=self.model,
            temperature=0,
        )
        simulated_output_response = simulated_output.choices[0].message.content
        assert simulated_output_response is not None, "Simulated output is None"
        assert isinstance(
            simulated_output_response, str
        ), "Simulated output is not a string"
        score = self.similarity(simulated_output_response, output)
        return score, simulated_output_response

    def similarity(self, text1: str, text2: str) -> float:
        vectorizer = TfidfVectorizer().fit_transform([text1, text2])
        vectors = vectorizer.toarray()
        cosine_sim = cosine_similarity(vectors[0:1], vectors[1:])
        score = cosine_sim[0][0]
        return 1 - score
