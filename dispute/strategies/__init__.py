

if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    os.environ["LOG_LEVEL"] = "DEBUG"

    import asyncio
    from LLMQuality import LLMQualityStrategy
    from ResponseSimilarity import ResponseSimilarityAnalysis
    from SemanticSimilarity import SemanticSimilarityAnalysis
    from StaticTextAnalysis import StaticTextAnalysisStrategy

    from config import MODELS, SIMULATION_MODEL

    input = "What is the capital of France?"
    output = "Paris"

    # LLM Quality
    lq = LLMQualityStrategy(
        models=MODELS
    )
    lq_result = asyncio.run(lq.analyze(input, output))
    print("LLM Quality: ", lq_result)

    # Response Similarity
    rs = ResponseSimilarityAnalysis(model=SIMULATION_MODEL)
    rs_result = asyncio.run(rs.analyze(input, output))
    print("Response Similarity:", rs_result)

    # Semantic Similarity
    ss = SemanticSimilarityAnalysis()
    ss_result = asyncio.run(ss.analyze(input, output))
    print("Semantic Similarity:", ss_result)

    # Static Text Analysis
    sta = StaticTextAnalysisStrategy()
    sta_result = sta.analyze(output)
    print("Static Text Analysis:", sta_result)



