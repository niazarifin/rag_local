"""
This is the Knowledge base.
    Analogy: a library shelf
    - stores chunks of raw text (static) in MongoDB
    - each chunk is a document, eg:
        {
            "chunk_id": 3,
            "text": "RAG reduces hallucinations by grounding answers...",
            "metadata": { "source": "demo" }
        }
    - does NOT modify chunks
    - does NOT combine them with questions
    - does NOT talk to the LLM
"""

from typing import List
from config import chunks_col

def seed_chunks(chunks: List[str], source: str = "demo") -> None:
    chunks_col.delete_many({}) # clears existing/old documents in MongoDB

    docs = []
    for i, text in enumerate(chunks):
        docs.append({
            "chunk_id": i,
            "text": text,
            "metadata": {"source": source},
        })

    chunks_col.insert_many(docs) # inserts new documents into MongoDB: stores each chunk as a document

if __name__ == "__main__":
    demo_chunks = [
        "RAG stands for Retrieval-Augmented Generation, a technique that combines information retrieval with text generation.",
        "RAG enhances Large Language Models by retrieving relevant external documents and injecting them into the prompt at inference time.",
        "RAG reduces hallucinations by grounding model responses in retrieved, authoritative context rather than relying solely on model memory.",
        "Vector search is used in RAG to retrieve the top-K most semantically relevant chunks for a given query.",
        "Chunking splits long documents into smaller, self-contained pieces so that retrieval can return precise context.",
        "In enterprise RAG systems, access control must be enforced before retrieval to ensure users only see permitted information.",
        "Prompt injection is a security risk in RAG systems where malicious instructions are embedded inside retrieved content.",
        "RAG acts like an open-book exam for an LLM, allowing it to look up relevant information before answering.",
        "RAG solves the limitation of LLMs having a fixed knowledge cutoff and no access to private or real-time data."
    ]
    seed_chunks(demo_chunks, source="rag_demo")
    print("✅ Seeded chunks:", chunks_col.count_documents({}))
