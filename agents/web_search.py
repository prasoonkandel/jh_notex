import json
import os

import numpy as np
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = os.getenv("OPENROUTER_API_URL")
EMBEDDING_API_URL = os.getenv("OPENROUTER_EMBEDDING_API_URL")

model = "google/gemini-3.8-flash"
embedding_model = "voyageai/voyage-4-lite"


def web_search(payload):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    # payload = {
    #     "query": {query},
    #     "numResults": {numResults},
    #     "contents": {"text": {"maxCharacters": {maxCharacters},
    # }

    response = requests.post(
        "https://ai.hackclub.com/proxy/v1/exa/search",
        headers=headers,
        json=payload,
    )

    for result in response.json()["results"]:
        print(result["title"], result["url"])
        print(result["text"])
