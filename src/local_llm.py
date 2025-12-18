"""
Module to interact with local LLM using Ollama.
    - sends prompts to the LLM
    - retrieves generated responses
"""

import ollama
from config import OLLAMA_MODEL

def generate(prompt: str, model: str | None = None) -> str:
    m = model or OLLAMA_MODEL
    resp = ollama.generate(model=m, prompt=prompt)
    return resp["response"]
