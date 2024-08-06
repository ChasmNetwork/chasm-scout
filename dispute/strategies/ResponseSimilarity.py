from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import asyncio
from util.llm import llm

class ResponseSimilarityAnalysis:
    def __init__(self, model: str):
        self.model = model

    async def analyze(self, input: str, output: str):
        loop = asyncio.get_event_loop()
        score = await loop.run_in_executor(None, self._sync_analyse, input, output)
        return score

    def _sync_analyse(self, input: str, output: str):

        simulated_output = llm.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": input},
            ],
            model=self.model,
            temperature=0.8,
        )
        simulated_output_response = simulated_output.choices[0].message.content
        assert simulated_output_response is not None, "Simulated output is None"
        score = self.similarity(simulated_output_response, output)
        return score

    def similarity(self, text1: str, text2: str) -> float:
        vectorizer = TfidfVectorizer().fit_transform([text1, text2])
        vectors = vectorizer.toarray()
        cosine_sim = cosine_similarity(vectors[0:1], vectors[1:])
        score = cosine_sim[0][0]
        return 1 - score
