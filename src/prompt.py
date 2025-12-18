"""
This module contains the prompt template used to query the language model.
Analogy: the instructions given to a helpful assistant.
It builds a prompt that includes:
    - a list of retrieved context chunks
    - the user's question
The prompt instructs the assistant to use only the provided context to answer the question.

context = retrieved_chunks
query = user question
"""

from typing import List

def build_prompt(query: str, retrieved_chunks: List[str]) -> str:
    context = "\n".join(f"- {c}" for c in retrieved_chunks)
    return f"""You are a helpful assistant.
    Use ONLY the context below to answer.
    If the answer is not in the context, say "I don't know."

    Context:
    {context}

    Question:
    {query}

    Answer:
    """
