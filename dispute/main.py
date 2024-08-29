from config import LOG_LEVEL, MIN_CONFIDENCE_SCORE
import asyncio
import os
from strategy import analyze_text
from util.chasm import ChasmConnection
import json
import logging

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

chasm = ChasmConnection()
PROCESSED_HISTORIES_FILE = "processed_histories.json"


def load_processed_histories():
    if os.path.exists(PROCESSED_HISTORIES_FILE):
        with open(PROCESSED_HISTORIES_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_processed_histories(histories):
    with open(PROCESSED_HISTORIES_FILE, "w") as f:
        json.dump(list(histories), f)


processed_histories = load_processed_histories()


async def process_histories():
    histories = chasm.get_prompt_history()
    logging.info(f"Histories: {len(histories)}")
    for history in histories:
        if history["_id"] in processed_histories:
            logging.debug(f"Skipping already processed history: {history['_id']}")
            continue
        output = history["result"]["choices"][0]["message"]["content"]
        result = await analyze_text(
            history["messages"],
            output,
            history["seed"],
            history["result"]["scout"]["provider"],
            history["result"]["scout"]["model"],
        )
        logging.debug(f"Result: {result}")
        logging.debug(f"Score: {result['confidence_score']}")

        if result["confidence_score"] > MIN_CONFIDENCE_SCORE:
            rs_output = result.get("rs_output")
            assert rs_output is not None, "rs_output is not generated"
            response = chasm.file_dispute(
                history["_id"],
                history["messages"],
                {"role": "assistant", "content": rs_output},
            )
            if response is not None:
                logging.info(f"Dispute filed: {response['result']}")

        # Cache history
        processed_histories.add(history["_id"])
        save_processed_histories(processed_histories)


async def main():
    while True:
        await process_histories()
        await asyncio.sleep(1)


if __name__ == "__main__":
    # set TOKENIZERS_PARALLELISM
    os.environ["TOKENIZERS_PARALLELISM"] = "true"
    asyncio.run(main())
