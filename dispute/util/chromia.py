import json
import time
from typing import List, Optional, Union
from pydantic import BaseModel
import requests
from requests.models import PreparedRequest

class PromptHistory(BaseModel):
    UID: int
    created_at: int
    messages: str
    model: str
    prompt_id: int
    provider: str
    result: str
    seed: int

class ChromiaDatabase:
    def __init__(self, base_url: Union[str, List[str]], brid = None):
        if isinstance(base_url, str):
            self.base_urls = [base_url]
        else:
            self.base_urls = base_url        
        self.brid = brid
    
    def set_brid(self, brid):
        self.brid = brid
    
    def _try_request(self, endpoint: str, params: Optional[dict] = None, headers: Optional[dict] = None) -> requests.Response:
        """
        Helper function to try making a request to multiple base URLs until one succeeds.
        
        :param endpoint: The API endpoint to append to the base URL.
        :param params: The query parameters to include in the request.
        :param headers: The headers to include in the request.
        :return: The successful requests.Response object.
        :raises Exception: If all requests fail.
        """
        for base_url in self.base_urls:
            try:
                url = f"{base_url}{endpoint}"
                req = PreparedRequest()
                req.prepare_url(url, params)
                response = requests.get(req.url, headers=headers)
                if response.status_code == 200:
                    return response
                else:
                    print(f"Failed to retrieve data from {base_url}. Status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Request to {base_url} failed: {e}")
        raise Exception("All base URLs failed to retrieve data.")

    def get_blockchain_brid(self, iid):
        response = self._try_request(endpoint=f"/brid/iid_{iid}", headers={"Content-Type": "text/plain"})
        return response.text
    
    def get_prompt_histories(self, start_time, end_time, pointer, n_prompts) -> (set[PromptHistory], int):
        response = self._try_request(
            endpoint=f"/query/{self.brid}",
            params={
                "type": "get_prompt_histories",
                "start_time": start_time,
                "end_time": end_time,
                "pointer": pointer,
                "n_prompts": n_prompts,
            },
            headers={"Content-Type": "application/json"}
        )
        data = response.json()
        return [PromptHistory(**x) for x in data["prompts"]], data["pointer"]

if __name__ == "__main__":
    base_url: str = ["https://dapps0.chromaway.com:7740"]
    brid = "BD8A4A23FD35BF0A711A8D65E94C06E651A286A412663A82AC2240416264C74D"
    chromia = ChromiaDatabase(base_url, brid)

    # Get prompt history
    current_time = round(time.time() * 1000)
    data, last_pointer = chromia.get_prompt_histories(
        start_time=-1,
        end_time=current_time,
        pointer = 0,
        n_prompts=20
    )
    if data is None or len(data) == 0:
        print("No data")
        exit()
    print(data[0])
    print(len(data))
    print(f"Last pointer: {last_pointer}")
