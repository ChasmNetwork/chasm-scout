from time import time
from typing import Literal, TypedDict, List
from openai.types.chat import ChatCompletionMessageParam
import requests
from urllib.parse import urljoin
from config import ORCHESTRATOR_URL, WEBHOOK_API_KEY
from util.fetch import request_with_backoff


class Message(TypedDict):
    role: Literal["user", "system", "assistant"]
    content: str


class Choice(TypedDict):
    message: Message
    scout: dict


class ScoutResult(TypedDict):
    model: str
    provider: str


class Result(TypedDict):
    model: str
    choices: list[Choice]
    scout: ScoutResult


class InferenceResult(TypedDict):
    input: list[ChatCompletionMessageParam]
    output: str
    answer: bool


class ChasmInferenceResult(TypedDict):
    _id: str
    UID: int
    messages: list[Message]
    result: Result
    seed: int


class ChasmConnection:
    def __init__(self) -> None:
        assert ORCHESTRATOR_URL is not None, "ORCHESTRATOR_URL is not set"
        self.base_url = ORCHESTRATOR_URL

    def file_dispute(self, id: str, input: List[Message], output: Message):
        url = urljoin(self.base_url, "/v1/dispute")
        print(f"Dispute URL: {url}")
        payload = {"id": id, "input": input, "output": output}
        headers = {"Authorization": f"Bearer {WEBHOOK_API_KEY}"}

        print(f"Dispute payload: {payload}")

        try:
            response = request_with_backoff(
                lambda: requests.post(url, json=payload, headers=headers)
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            response = http_err.response.json()
            if response.get("error"):
                print(f"Error filing dispute: {response.get('error')}")
            else:
                print(f"HTTP error occured: {http_err}")
        except Exception as err:
            print(f"Error occured: {err}")

    def get_prompt_history(self, page_size=20) -> list[ChasmInferenceResult]:
        time_now = time()

        url = urljoin(self.base_url, f"/scouts/prompts?page=1&pageSize={page_size}")
        print(url)
        response = requests.get(
            url, headers={"Authorization": f"Bearer {WEBHOOK_API_KEY}"}
        )
        response.raise_for_status()

        time_after = time()
        print(f"Time taken: {time_after - time_now}s")

        response_json = response.json()
        return response_json["data"]

    def get_benchmark_test(self) -> list[InferenceResult]:
        return [
            # OpenAI
            # https://platform.openai.com/docs/examples
            {
                "input": [
                    {
                        "role": "system",
                        "content": "You will be provided with statements, and your task is to convert them to standard English.",
                    },
                    {"role": "user", "content": "She no went to the market."},
                ],
                "output": "She did not go to the market.",
                "answer": True,
            },
            {
                "input": [
                    {
                        "role": "system",
                        "content": "Summarize the following text for a second-grade student.",
                    },
                    {
                        "role": "user",
                        "content": "Jupiter is the fifth planet from the Sun and the largest in the Solar System. It is a gas giant with a mass one-thousandth that of the Sun, but two-and-a-half times that of all the other planets in the Solar System combined. Jupiter is one of the brightest objects visible to the naked eye in the night sky, and has been known to ancient civilizations since before recorded history. It is named after the Roman god Jupiter.[19] When viewed from Earth, Jupiter can be bright enough for its reflected light to cast visible shadows,[20] and is on average the third-brightest natural object in the night sky after the Moon and Venus.",
                    },
                ],
                "output": "Jupiter is a really big planet in our Solar System. It is the fifth planet from the Sun and it is the largest planet. It is called a gas giant because it is made mostly of gas. Jupiter is much smaller than the Sun, but it is bigger than all the other planets combined. It is very bright and can be seen in the night sky without a telescope. People have known about Jupiter for a very long time, even before they started writing things down. It is named after a god from ancient Rome. Sometimes, Jupiter is so bright that it can make shadows on Earth. It is usually the third-brightest thing we can see in the night sky, after the Moon and Venus.",
                "answer": True,
            },
            {
                "input": [
                    {
                        "role": "system",
                        "content": "You will be provided with text, and your task is to translate it into emojis. Do not use any regular text. Do your best with emojis only.",
                    },
                    {
                        "role": "user",
                        "content": "Artificial intelligence is a technology with great promise.",
                    },
                ],
                "output": "🤖🧠📈",
                "answer": True,
            },
            {
                "input": [
                    {
                        "role": "system",
                        "content": "You will be provided with a tweet, and your task is to classify its sentiment as positive, neutral, or negative.",
                    },
                    {
                        "role": "user",
                        "content": "I loved the new Batman movie!",
                    },
                ],
                "output": "negative",
                "answer": False,
            },
            # KILT TriviaQA Judge Prompt
            # True
            {
                "input": [
                    {
                        "role": "user",
                        "content": """Which American played in his 10th Ryder Cup in 2014?
            Provided Answer: "Mickelson extended his own U.S. team record with his 10th appearance at the 2014 Ryder Cup.""",
                    }
                ],
                "output": "philip alfred mickelson",
                "answer": True,
            },
            # False
            {
                "input": [
                    {
                        "role": "user",
                        "content": """If you landed at ’Santa Catarina Airport on which Island would you be in?
            Provided Answer: If you landed at Santa Catarina Airport, you would be on the island of Santa Catarina, in the Brazilian state of the same name. The island is approximately 54km long and 18km wide and is home to the state capital, Florianópolis. It is the largest island in an archipelago of over 30 islands.""",
                    }
                ],
                "output": "Geography of the Madeira Islands",
                "answer": False,
            },
            # False
            {
                "input": [
                    {
                        "role": "user",
                        "content": """The religious order of Poor Ladies of San Damiano has what more common name?" Provided Answer: "The religious order of Poor Ladies of San Damiano is more commonly known
            as the Poor Clares. This order was founded by Saints Clare of Assisi and Francis of Assisi in 1212, and it was the second Franciscan Order to be established. The Poor Clares were
            initially referred to as the Order of Poor Ladies, and later the Clarisses, the Minoresses, the Franciscan Clarist Order, and the Second Order of Saint Francis. However, the name Poor
            Clares is the most recognized and widely used today.""",
                    }
                ],
                "output": "Franciscan Clarist Order",
                "answer": False,
            },
            # False
            {
                "input": [
                    {
                        "role": "user",
                        "content": """Fred Scuttle was one of the best-known characters of which British comedian?
            Provided Answer: "The provided documents do not directly mention Fred Scuttle or the British comedian associated with this character. Therefore, based on the information available in the documents, it is not possible to accurately answer the question about which British comedian is best known for the character Fred Scuttle.""",
                    }
                ],
                "output": "Alfred Hawthorne Hill",
                "answer": False,
            },
            # ShareGPT Dataset from Vicuna (Expected True)
            # https://huggingface.co/datasets/anon8231489123/ShareGPT_Vicuna_unfiltered
            {
                "input": [
                    {
                        "role": "user",
                        "content": 'In Java, I want to replace string like "This is a new {object} at {place}" with a Map, {object: "student", "point 3, 4"}, and get a result "This is a new student at point 3, 4". How can I do?',
                    }
                ],
                "output": 'You can use the `String.format()` method in Java to replace placeholders in a string with values from a map. Here\'s an example code snippet that demonstrates how you can achieve this:\n```java\nimport java.util.HashMap;\nimport java.util.Map;\n\npublic class StringReplaceExample {\n    public static void main(String[] args) {\n        String input = "This is a new {object} at {place}";\n        Map<String, String> replacements = new HashMap<>();\n        replacements.put("object", "student");\n        replacements.put("place", "point 3, 4");\n\n        String output = replacePlaceholders(input, replacements);\n        System.out.println(output);\n    }\n\n    public static String replacePlaceholders(String input, Map<String, String> replacements) {\n        for (Map.Entry<String, String> entry : replacements.entrySet()) {\n            String placeholder = "{" + entry.getKey() + "}";\n            String replacement = entry.getValue();\n            input = input.replace(placeholder, replacement);\n        }\n        return input;\n    }\n}\n```\nIn this example, we define the input string as "This is a new {object} at {place}", and create a `HashMap` called `replacements` that maps the placeholders "object" and "place" to their corresponding values "student" and "point 3, 4". We then pass these values to the `replacePlaceholders()` method, which iterates over the entries in the `replacements` map and replaces each placeholder in the input string with its corresponding value using the `replace()` method. Finally, the `replacePlaceholders()` method returns the modified string, which is printed to the console.\n\nThe output of this program will be:\n```csharp\nThis is a new student at point 3, 4\n```\nNote that you can modify the `replacements` map to include additional placeholders and their corresponding values, and the `replacePlaceholders()` method will automatically replace them in the input string.',
                "answer": True,
            },
            {
                "input": [
                    {
                        "role": "user",
                        "content": 'I have the following C++ function: \nvoid add\\_player(vector& players)\n{\n string player\\_name;\n string player\\_class;\n string dummy;\n PlayerClass pc;\n string player\\_sex;\n int player\\_gold;\n\n cout << " Create a Mage, Warrior, Bowman, or Thief" << endl;\n\n cout << "Name: ";\n getline(cin, player\\_name);\n\n cout << "Class: ";\n getline(cin, player\\_class);\n pc = get\\_player\\_class\\_from\\_string(player\\_class);\n while (pc == PlayerClass::InvalidPlayerClass)\n {\n cout << " Invalid class, try again" << endl;\n cout << "Class: ";\n getline(cin, player\\_class);\n pc = get\\_player\\_class\\_from\\_string(player\\_class);\n }\n\n cout << "Sex: ";\n getline(cin, player\\_sex);\n\n cout << "Gold: ";\n cin >> player\\_gold;\n getline(cin, dummy); //consume newline\n\n GamePlayer new\\_player;\n new\\_player.name = player\\_name;\n new\\_player.occupation = pc;\n new\\_player.gender = player\\_sex;\n new\\_player.gold = player\\_gold;\n\n //add to vector\n players.push\\_back(new\\_player);\n\n //add to file\n write\\_players\\_file(players);\n}\nCan you explain to me how the dummy variable is being used?',
                    }
                ],
                "output": "The `dummy` variable in the given C++ function is being used to consume the newline character left in the input stream after the `player_gold` integer is read using the `cin` statement.\n\nThis is because when an integer is read using `cin`, it only reads the integer value and leaves the newline character (`\\n`) in the input stream. So when the `getline` function is called to read the `player_sex` string, it immediately reads the newline character left in the input stream and stops reading, resulting in an empty string being stored in the `player_sex` variable.\n\nTo avoid this issue, the `getline` function is called again after reading the integer value, this time storing the input in the `dummy` variable. Since `dummy` is not used anywhere else in the function, it serves only to consume the leftover newline character and allow the next `getline` call to read the correct input.",
                "answer": True,
            },
        ]
