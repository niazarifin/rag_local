"""
This is the Retriever module.
Analogy: a librarian fetching books from the shelf.
    - retrieves top-K relevant chunks from the knowledge base given a query
    - uses a simple hash-based embedding for demonstration purposes
    - takes a user question
    - finds the most relevant chunks
    - returns them as plain text
"""

from typing import List, Tuple
import numpy as np
from config import chunks_col

def _simple_hash_embedding(text: str, dim: int = 256) -> np.ndarray:
    v = np.zeros(dim, dtype=np.float32)
    for tok in text.lower().split():
        h = hash(tok) % dim
        v[h] += 1.0
    return v / (np.linalg.norm(v) + 1e-12)

def retrieve_top_k(query: str, k: int = 3) -> Tuple[List[str], List[float]]:
    # MongoDB does not rank or embed — it just supplies text.
    # Analogy: the librarian fetches books, but does not read them.
    # Give me all the books so I can decide which ones are relevant.
    
    rows = list(chunks_col.find({}, {"_id": 0, "text": 1})) # fetches all documents from MongoDB: MongoDB READ
    if not rows:
        raise RuntimeError("No chunks found. Run store.py first.")

    texts = [r["text"] for r in rows]
    doc_vecs = np.stack([_simple_hash_embedding(t) for t in texts])
    qvec = _simple_hash_embedding(query)

    sims = doc_vecs @ qvec
    idx = np.argsort(-sims)[:k]

    return [texts[i] for i in idx], [float(sims[i]) for i in idx]

if __name__ == "__main__":
    q = "What is Retrieval-Augmented Generation (RAG)?"
    # "How does RAG reduce hallucinations?"  
    # What is RAG?
    #"How does doctor reduce fever?"
    print(f"🔍 Query: {q}\n")
    chunks, scores = retrieve_top_k(q, k=2)
    for c, s in zip(chunks, scores):
        print(f"[{s:.4f}] {c}")