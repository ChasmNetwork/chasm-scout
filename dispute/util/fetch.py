import time
import random
from typing import Callable
import requests


def request_with_backoff(request_func: Callable[[], requests.Response], max_retries=3):
    retry_delay = 1  # Initial delay in seconds
    for _ in range(max_retries):
        try:
            response = request_func()
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            time.sleep(retry_delay)
            retry_delay *= 2  # Double the delay for the next attempt
            retry_delay += random.uniform(0, 1)  # Add jitter

    raise Exception("Maximum retry attempts reached")
