import asyncio
from datetime import datetime
from typing import TypedDict
import logging
from config import SIMULATION_MODEL, MODELS
from strategies.ResponseSimilarity import ResponseSimilarityAnalysis
from strategies.LLMQuality import LLMQualityStrategy
from strategies.StaticTextAnalysis import StaticTextAnalysisStrategy
from strategies.SemanticSimilarity import SemanticSimilarityAnalysis


class TextAnalysisResult(TypedDict):
    ss_score: float
    llm_score: float
    rs_score: float
    confidence_score: float
    correct: bool
    dispute: bool


async def analyze_text(input: str, output: str) -> TextAnalysisResult:
    """
    Analyze the given input and output texts to determine scores and dispute status.

    Args:
        input (str): The input text to analyze.
        output (str): The output text to analyze.

    Returns:
        dict: A dictionary containing the gibberish text score, semantic similarity score,
              LLM quality score, the final confidence score, and dispute status.
    """
    try:
        start_time = datetime.now()

        # 1. Empty Text
        sta_strategy = StaticTextAnalysisStrategy()
        sta_result = sta_strategy.analyze(output)
        if sta_result:
            return {
                "confidence_score": 1.0,
                "dispute": True,
                "correct": False,
                "ss_score": 1.0,
                "llm_score": 1.0,
                "rs_score": 1.0,
            }

        # 2. Semantic Similarity
        ss_strategy = SemanticSimilarityAnalysis()

        # 3. LLM Analysis
        llm_strategy = LLMQualityStrategy(models=MODELS)

        # 4. Response
        rs_strategy = ResponseSimilarityAnalysis(model=SIMULATION_MODEL)

        # Gather scores concurrently
        scores = await asyncio.gather(
            ss_strategy.analyze(input, output),
            llm_strategy.analyze(input, output),
            rs_strategy.analyze(input, output),
        )
        ss_score, llm_score, rs_score = scores

        # Final Score Calculation
        confidence_score = (llm_score * 0.5) + (ss_score * 0.1) + (rs_score * 0.4)

        time_diff = datetime.now() - start_time
        print(f"Time taken: {time_diff}")

        dispute = confidence_score > 0.5

        return {
            "ss_score": ss_score,
            "llm_score": llm_score,
            "rs_score": rs_score,
            "confidence_score": confidence_score,
            "dispute": dispute,
            "correct": not dispute,
        }

    except Exception as e:
        logging.error(f"Error in analyze_text: {e}")
        # Default to no dispute
        return {
            "ss_score": 0.0,
            "llm_score": 0.0,
            "rs_score": 0.0,
            "confidence_score": 0.0,
            "dispute": False,
            "correct": True,
        }
