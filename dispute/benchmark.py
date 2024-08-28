import dotenv

dotenv.load_dotenv()

import asyncio
from util.chasm import ChasmConnection
from strategy import analyze_text


async def main():
    connection = ChasmConnection()
    histories = connection.get_benchmark_test()
    i = 0
    for history in histories:
        print(f"--- {i} ---")
        result = await analyze_text(
            history["input"], history["output"], 0, "openai", "gpt-3"
        )
        print(f"Result: {result}")
        print(f"Score: {result['confidence_score']}")
        print(
            f"Assert Check: {'✅' if result['correct'] == history['answer'] else '❌'}"
        )
        print(f"Dispute: {result['dispute']}")
        i += 1
    pass


if __name__ == "__main__":
    # set TOKENIZERS_PARALLELISM
    import os

    os.environ["TOKENIZERS_PARALLELISM"] = "true"
    asyncio.run(main())

