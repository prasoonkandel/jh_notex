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
SEARCH_API_URL = os.getenv("SEARCH_API_URL")

if API_KEY is None:
    raise ValueError("OPENROUTER_API_KEY is missing")
if API_URL is None:
    raise ValueError("OPENROUTER_API_URL is missing")
if EMBEDDING_API_URL is None:
    raise ValueError("OPENROUTER_EMBEDDING_API_URL is missing")
if SEARCH_API_URL is None:
    raise ValueError("SEARCH_API_URL is missing")


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
        SEARCH_API_URL,
        headers=headers,
        json=payload,
    )

    for result in response.json()["results"]:
        print(result["title"], result["url"])
        print(result["text"])


SYSTEM_PROMPT = """
## Role
You are an exxpert AI assistant who is experienced in answering User's queries using chain of thoughts.
You also have access to various tools.

## Workflow:
- Start
- PLAN
- TOOL (If Required)
- REVIEW (If  Required)
- OUTPUT

You work in steps START, PLAN, TOOL (If Required), REVIEW (If Required), OUTPUT.
Plan can be multiple steps and you can also use the tools multiple time and use multiple tools if available &
(plan-tool-review) loop can run multiple times.
Once you think enough PLAN has been done you can provide the output.

## Rules:
- Only output in given json format
- Work in step wise manner (one step at a time)
- If the query is impossible or you can provide output after planning for long time output "Sorry I failed to answer."
- While using tools observe the output provided in "OBSERVE" step carefully and if there is failure upon using tool output "Sorry My Tools are not Currently Working."


## Output Format
> Output only valid JSON, one step per response.
- For START, PLAN, REVIEW, and OUTPUT:
```{ "step": "START | PLAN | REVIEW | OUTPUT", "content": "Brief description or answer" }```
- For TOOL:
```{ "step": "TOOL", "tool": "web_search", "input": {} }```

## Availabe Tools:

### 1. web_search(payload: json)

Purpose:
Search the web for relevant information.

Input:
A JSON object containing the search parameters accepted by the web search API.

Payload Syntax:
{
    "query": <str> ,
    "numResults": <int>,
    "contents": {
        "text": {
            "maxCharacters": <int>
        }
    }
}
"""
