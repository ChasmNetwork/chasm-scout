import asyncio
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SemanticSimilarityAnalysis:
    def __init__(self):
        pass

    async def analyze(self, input: str, output: str) -> float:
        loop = asyncio.get_event_loop()
        score = await loop.run_in_executor(None, self._sync_analyze, input, output)
        return score

    def _sync_analyze(self, input: str, output: str) -> float:
        vectorizer = TfidfVectorizer().fit_transform([input, output])
        vectors = vectorizer.toarray()
        cosine_sim = cosine_similarity(vectors[0:1], vectors[1:])
        score = cosine_sim[0][0]
        return 1 - score