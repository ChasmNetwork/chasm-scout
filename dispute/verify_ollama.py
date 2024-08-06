import json
from math import e
from dotenv import load_dotenv
load_dotenv()

from config import LLM_BASE_URL, MODELS, SIMULATION_MODEL

import requests

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"


if __name__ == "__main__":
    base_url = LLM_BASE_URL.replace("/v1", "")
    try: 
        tags_url = f"{base_url}/api/tags"
        print(tags_url)
        print("---")
        response = requests.get(tags_url, headers={"x-api-key": "ollama"})
        response.raise_for_status()  

        # If the response is not 200, raise an exception
        if response.status_code != 200:
            raise ValueError(f"Error: {response.text}")
        
        response_json = json.loads(response.text)
        available_models = map(lambda x: x["model"], response_json["models"])

        for model in MODELS:
            if model not in available_models:
                raise ValueError(f"{RED}[OLLAMA ERROR] Model {model} not available in the API, please run `ollama pull {model}`{RESET}")
            
        if SIMULATION_MODEL not in MODELS:
            raise ValueError(f"{RED}[OLLAMA ERROR] Simulation model {SIMULATION_MODEL} not available in the MODELS list, please run `ollama pull {SIMULATION_MODEL}`{RESET}")
    
        print(f"{GREEN}[SUCCESS] Ollama API is available and models are correctly configured{RESET}")
        exit(0)
        
    except requests.exceptions.HTTPError as http_err:
        print(f"{RED}[HTTP ERROR] HTTP error occurred: {http_err}{RESET}")
        exit(1)
    except requests.exceptions.RequestException as req_err:
        print(f"{RED}[REQUEST ERROR] Request error occurred: {req_err}{RESET}")
        exit(1)
    except ValueError as val_err:
        print(f"{RED}[VALUE ERROR] Value error: {val_err}{RESET}")
        exit(1)
    except Exception as err:
        print(f"{RED}[UNKNOWN ERROR] An error occurred: {err}{RESET}")
        exit(1)

