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


model = "~openai/gpt-mini-latest"
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

    response.raise_for_status()

    return response.json()["results"]


available_tools = {"web_search": web_search}

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
- Always start from START step and PLAN before OUTPUT
- Never give direct OUTPUT
- Use Tools if you are not confident
- Only output in given json format
- Work in step wise manner (one step at a time)
- While using tools observe the output provided in "OBSERVE" step carefully and if there is failure upon using tool output "Sorry My Tools are not Currently Working."
- Do not ever ask user follow up questions
- Always use successfully retrieved search results as evidence; never claim tools failed if they executed successfully and returned results.
- Answer confidently using facts explicitly supported by reliable sources, citing URLs when available; avoid unnecessary disclaimers.
- If evidence is incomplete or conflicting, provide the supported information and clearly identify only what remains uncertain.

## Output Format
> Output only valid JSON, one step per response.
- For START, PLAN, REVIEW, and OUTPUT:
{ "step": "START | PLAN | REVIEW | OUTPUT", "content": "Brief description or answer" }
- For TOOL:
{ "step": "TOOL", "tool": "web_search", "input": {} }

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

Instructions:
If you used this search tool please provide user summmary of full information rather than just telling I can not find reliable information.
"""


memory = []

memory.append({"role": "system", "content": SYSTEM_PROMPT})


def answer(query: str):
    memory.append({"role": "user", "content": query})

    while True:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": model,
            "messages": memory,
            "temperature": 0.2,
            "max_tokens": 3000,
            "response_format": {"type": "json_object"},
        }
        response = requests.post(API_URL, headers=headers, json=payload)

        if not response.ok:
            print("Status:", response.status_code)
            print("Error:", response.text)
            response.raise_for_status()

        response.raise_for_status()

        result = json.loads(response.json()["choices"][0]["message"]["content"].strip())

        print(result)

        memory.append({"role": "assistant", "content": json.dumps(result)})

        if result["step"] == "TOOL":
            try:
                output = available_tools[result["tool"]](result["input"])

                if not output:
                    observation = {
                        "step": "OBSERVE",
                        "success": True,
                        "content": "Search completed, but returned no results.",
                    }
                else:
                    observation = {
                        "step": "OBSERVE",
                        "success": True,
                        "content": output,
                    }

            except Exception as e:
                observation = {
                    "step": "OBSERVE",
                    "success": False,
                    "content": str(e),
                }

            memory.append(
                {
                    "role": "user",
                    "content": json.dumps(observation, default=str),
                }
            )

        elif result["step"] == "OUTPUT":
            print("Output:", result["content"])
            return result["content"]

        elif result["step"] in ("START", "PLAN", "REVIEW"):
            continue

        else:
            raise ValueError(f"Unknown step: {result['step']}")
