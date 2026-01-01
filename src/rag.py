"""
RAG pipeline module.
Analogy: a librarian fetching books from the shelf and then asking a helpful assistant to summarize them.
    - retrieves top-K relevant chunks from the knowledge base given a query
    - uses a simple hash-based embedding for demonstration purposes
    - takes a user question
    - finds the most relevant chunks
    - returns them as plain text
"""

import sys
from store import seed_chunks
from retrieve import retrieve_top_k
from prompt import build_prompt
from local_llm import generate

def rag_answer(query: str, k: int = 3) -> str:
    chunks, scores = retrieve_top_k(query, k)

    print("\n=== Retrieved Context ===")
    for c, s in zip(chunks, scores):
        print(f"[{s:.4f}] {c}")

    print("\n=== Generating Answer... ===\n\n")
    prompt = build_prompt(query, chunks)
    return generate(prompt)

if __name__ == "__main__":
    q = input("Ask a question: ").strip() or "How does RAG reduce hallucinations?"
    print("\n=== Answer ===")
    print(rag_answer(q))

    sys.exit(0)

# Ask a question: what is RAG?
# Ask a question: How does RAG work?

# That “stuck” moment is almost certainly Ollama still generating — 
# your program has already printed retrieval, and it’s now waiting for ollama.generate(...) to return. 
# For some models / first run, that can take a while (model load + generation).