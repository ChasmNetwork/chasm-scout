import re
import logging
from util.poll import PollAlgo
from strategies.tokenizer import Tokenizer


class LLMQualityStrategy:
    def __init__(self, models):

        # llama3 tokenizer
        self.tokenizer = Tokenizer()
        self.poll = PollAlgo(models)

    def format_text_limit(self, text: str, limit: int):
        encoded_result = self.tokenizer.encode(text, bos=False, eos=False)
        return self.tokenizer.decode(encoded_result[:limit])

    async def analyze(self, input: str, output: str):
        input = self.format_text_limit(input, 3000)
        output = self.format_text_limit(output, 3000)

        # Prompt from https://arxiv.org/abs/2306.05685v4
        results = await self.poll.create_poll_completion(
            messages=[
                {
                    "role": "system",
                    "content": """You are judging whether a model has generated a correct answer to a question. 
Study the examples the user gives you as they will be very informative for how to do the task.
Don’t worry about factuality with respect to the real world, just judge the example based on what you see. 
No need to overthink this task, it really comes down to just soft matching.                     
If the Provided Answer is correct say exactly "True", otherwise say "False". 
Only answer the question, do not provide supporting exposition.
""",
                },
                {
                    "role": "user",
                    "content": """Question: What element is the main constituent of anthracite?
Provided Answer: The main constituent of anthracite is carbon. High-grade anthracite, for example, has a chemical formula represented by CHONS, indicating it contains carbon, hydrogen, oxygen, nitrogen, and sulfur, with carbon making up 94% of its composition. Ultra high-grade (UHG) anthracite typically has a minimum carbon content of 95%, further emphasizing carbon as the primary element in anthracite.
Answer: Carbon
""",
                },
                {"role": "assistant", "content": "True"},
                {
                    "role": "user",
                    "content": """Question: The religious order of Poor Ladies of San Damiano has what more common name?
Provided Answer: The religious order of Poor Ladies of San Damiano is more commonly known as the Poor Clares. This order was founded by Saints Clare of Assisi and Francis of Assisi in 1212, and it was the second Franciscan Order to be established. The Poor Clares were initially referred to as the Order of Poor Ladies, and later the Clarisses, the Minoresses, the Franciscan Clarist Order, and the Second Order of Saint Francis. However, the name Poor Clares is the most recognized and widely used today.
Answer: Franciscan Clarist Order
""",
                },
                {"role": "assistant", "content": "False"},
                {"role": "user", "content": f"Question: {input}\nAnswer: {output}"},
            ],
        )
        logging.debug(results)
        llm_results = []

        for r in results:
            assert r is not None, "LLM returned None"
            r_lower = r.lower()
            if "true" in r_lower and "false" in r_lower:
                true_index = re.search(r"\btrue\b", r_lower).start()
                false_index = re.search(r"\bfalse\b", r_lower).start()
                llm_results.append(0 if true_index < false_index else 1)
            elif "true" in r_lower:
                llm_results.append(0)
            elif "false" in r_lower:
                llm_results.append(1)
            elif "yes" in r_lower:
                llm_results.append(0)
            elif "no" in r_lower:
                llm_results.append(1)
            else:
                llm_results.append(0.5)
        logging.debug(f"LLM Results: {llm_results}")
        score = sum(llm_results) / len(llm_results)
        return score
