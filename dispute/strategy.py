from datetime import datetime
from typing import List, Optional, TypedDict
import logging

from config import (
    GROQ_API_KEY,
    MIN_CONFIDENCE_SCORE,
    MIN_RESPONSE_DIFFERENCE,
    OPENROUTER_API_KEY,
    SIMULATION_MODEL,
    MODELS,
)
from util.chasm import Message
from strategies.ResponseSimilarity import ResponseSimilarityAnalysis
from strategies.LLMQuality import LLMQualityStrategy
from strategies.StaticTextAnalysis import StaticTextAnalysisStrategy
from strategies.ResponseRecompute import ResponseRecomputeAnalysis


class TextAnalysisResult(TypedDict):
    llm_score: float
    rs_score: float
    confidence_score: float
    correct: bool
    dispute: bool
    rs_output: Optional[str]


async def analyze_text(
    input: List[Message],
    output: str,
    seed: int,
    provider: str,
    model: str,
) -> TextAnalysisResult:
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
                "llm_score": 1.0,
                "rs_output": None,
                "rs_score": 1.0,
            }

        # 2. LLM Analysis
        llm_strategy = LLMQualityStrategy(models=MODELS)
        llm_score = await llm_strategy.analyze(input, output)

        print(f"LLM Score: {llm_score}")
        if llm_score > 0.5:
            return {
                "confidence_score": 0.0,
                "dispute": False,
                "correct": True,
                "llm_score": llm_score,
                "rs_output": None,
                "rs_score": 0.0,
            }

        # 3. Response
        rs_strategy = ResponseSimilarityAnalysis(model=SIMULATION_MODEL)
        rs_result = await rs_strategy.analyze(input, output)
        rs_score, rs_output = rs_result

        print(f"RS Score: {rs_score}")

        # Final Score Calculation
        confidence_score = (llm_score * 0.5) + (rs_score * 0.5)

        time_diff = datetime.now() - start_time
        print(f"Time taken: {time_diff}")

        dispute = confidence_score > MIN_CONFIDENCE_SCORE

        recomputable_provider = True if provider in ["groq", "openrouter"] else False

        # Try to recompute the output
        if GROQ_API_KEY and OPENROUTER_API_KEY and dispute and recomputable_provider:
            rr_strategy = ResponseRecomputeAnalysis(model=model)
            print("Dispute detected. Trying to recompute...")
            recompute_result = await rr_strategy.analyse(input, output, seed, provider)
            if recompute_result:
                rs_score, _ = recompute_result
                if rs_score < MIN_RESPONSE_DIFFERENCE:
                    return {
                        "llm_score": llm_score,
                        "rs_score": rs_score,
                        "rs_output": rs_output,
                        "confidence_score": confidence_score,
                        "dispute": dispute,
                        "correct": False,
                    }

        return {
            "llm_score": llm_score,
            "rs_score": rs_score,
            "rs_output": rs_output,
            "confidence_score": confidence_score,
            "dispute": dispute,
            "correct": not dispute,
        }

    except Exception as e:
        logging.error(f"Error in analyze_text: {e}")
        # Default to no dispute
        return {
            "llm_score": 0.0,
            "rs_score": 0.0,
            "rs_output": None,
            "confidence_score": 0.0,
            "dispute": False,
            "correct": True,
        }
