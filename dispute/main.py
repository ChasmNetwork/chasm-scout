from config import LOG_LEVEL, MIN_CONFIDENCE_SCORE
import asyncio
import os
from util.chromia import ChromiaDatabase
from strategy import analyze_text
from util.chasm import ChasmConnection
import json
import logging
import time

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

chasm = ChasmConnection()
chromia = ChromiaDatabase(
    base_url=[
      "https://dapps0.chromaway.com:7740",
      "https://chromia-mainnet.w3coins.io:7740",
      "https://mainnet-dapp1.sunube.net:7740",
      "https://chromia.01node.com:7740",
      "https://chromia-mainnet.caliber.build:443",
      "https://chromia.nocturnallabs.org:7740",
      "https://chromia2.stablelab.cloud:7740",
    ],
    brid="BD8A4A23FD35BF0A711A8D65E94C06E651A286A412663A82AC2240416264C74D"
)
PROCESSED_HISTORIES_FILE = "processed_histories_chromia.json"


def load_processed_histories():
    if os.path.exists(PROCESSED_HISTORIES_FILE):
        try:
            with open(PROCESSED_HISTORIES_FILE, "r") as f:
                return json.load(f)
        except:
            return set()
    return set()


def save_processed_histories(histories):
    with open(PROCESSED_HISTORIES_FILE, "w") as f:
        json.dump(list(histories), f)

async def process_histories(pointer):
    processed_histories = load_processed_histories()
    processed_histories_prompt_ids = set(map(lambda x: x[0], processed_histories))
    start_time = -1
    if len(processed_histories) > 0:
        start_time = max(map(lambda x: x[1], processed_histories))
    current_time = round(time.time() * 1000)
    histories, last_pointer = chromia.get_prompt_histories(
        start_time,
        end_time=current_time,
        pointer=pointer,
        n_prompts=50
    )

    logging.info(f"Histories: {len(histories)}")
    for history in histories:
        prompt_id = history.prompt_id
        if prompt_id in processed_histories_prompt_ids:
            logging.debug(f"Skipping already processed history: {history['_id']}")
            continue
        logging.debug(f"Processing history: {prompt_id}")
        created_at = history.created_at
        seed = history.seed
        provider = history.provider
        model = history.model
        messages = json.loads(history.messages)
        result = json.loads(history.result)
        input = map(lambda x: x["content"], messages)
        input = "\n".join(input)
        output = result["choices"][0]["message"]["content"]
        res = await analyze_text(
            messages,
            output,
            seed,
            provider,
            model
        )
        logging.debug(f"Result: {res}")
        logging.debug(f"Score: {res['confidence_score']}")

        if res["confidence_score"] > MIN_CONFIDENCE_SCORE:
            rs_output = res.get("rs_output")
            assert rs_output is not None, "rs_output is not generated"
            response = chasm.file_dispute(
                prompt_id,
                messages,
                {"role": "assistant", "content": rs_output},
            )
            if response is not None:
                logging.info(f"Dispute filed: {response['result']}")

        # Cache history
        processed_histories.add((
            prompt_id,
            created_at,
        ))
        save_processed_histories(processed_histories)
    return last_pointer


async def main():
    history_pointer = 0
    while True:
        history_pointer = await process_histories(history_pointer)
        await asyncio.sleep(1)


if __name__ == "__main__":
    # set TOKENIZERS_PARALLELISM
    os.environ["TOKENIZERS_PARALLELISM"] = "true"
    asyncio.run(main())
