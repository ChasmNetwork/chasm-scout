from typing import List


if __name__ == "__main__":
    import sys
    import os

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

    os.environ["LOG_LEVEL"] = "DEBUG"

    import asyncio
    from LLMQuality import LLMQualityStrategy
    from ResponseSimilarity import ResponseSimilarityAnalysis
    from SemanticSimilarity import SemanticSimilarityAnalysis
    from ResponseRecompute import ResponseRecomputeAnalysis
    from StaticTextAnalysis import StaticTextAnalysisStrategy
    from util.chasm import Message

    from config import MODELS, SIMULATION_MODEL

    input: List[Message] = [
        {"role": "user", "content": "What is the capital of France?"}
    ]
    output = "Paris"

    # LLM Quality
    lq = LLMQualityStrategy(models=MODELS)
    lq_result = asyncio.run(lq.analyze(input, output))
    print("LLM Quality: ", lq_result)

    # Response Similarity
    rs = ResponseSimilarityAnalysis(model=SIMULATION_MODEL)
    rs_result = asyncio.run(rs.analyze(input, output))
    print("Response Similarity:", rs_result)

    # Semantic Similarity
    ss = SemanticSimilarityAnalysis()
    text_input = map(lambda x: x["content"], input)
    text_input = "\n".join(text_input)
    ss_result = asyncio.run(ss.analyze(text_input, output))
    print("Semantic Similarity:", ss_result)

    # Static Text Analysis
    sta = StaticTextAnalysisStrategy()
    sta_result = sta.analyze(output)
    print("Static Text Analysis:", sta_result)

    # Response Recompute Analysis
    rra = ResponseRecomputeAnalysis(model=SIMULATION_MODEL)
    rra_result = asyncio.run(rra.analyse(input, output, 42, "groq"))
    print("Response Recompute Analysis:", rra_result)
