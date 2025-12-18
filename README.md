# RAG Local — Minimal Retrieval-Augmented Generation Demo

This repository implements a small, self-contained Retrieval-Augmented Generation (RAG) demo that uses a MongoDB-backed knowledge store and a local LLM (via Ollama) for generation.

<img width="821" height="471" alt="rag_llm_local drawio" src="https://github.com/user-attachments/assets/6c455b22-27fe-4cf6-85a4-4bf418bb6fa2" />


Files
-	requirements.txt — Python dependencies (numpy, pymongo, python-dotenv, certifi, ollama, dnspython).
-	.env — Environment variables (not committed). See "Environment" below for required keys.
-	src/config.py — Loads environment variables and creates a MongoDB client and collection handle. Exposes `chunks_col` for other modules. Required env vars: `MONGODB_URI`. Optional: `OLLAMA_MODEL`, `DB_NAME`, `COLLECTION_NAME`.
-	src/store.py — Knowledge base seeding module. Inserts demo text chunks into MongoDB. Use this to populate the `chunks` collection. Does not call the LLM.
-	src/retrieve.py — Retriever module. Implements a simple hash-based embedding and returns the top-K most similar text chunks for a query. For demo purposes only (not production-grade embeddings).
-	src/prompt.py — Prompt template builder. Formats retrieved chunks together with the user question into a prompt instructing the assistant to answer only from the provided context.
-	src/local_llm.py — LLM adapter for local Ollama. Sends prompts to Ollama via the `ollama` Python client and returns the generated response. Requires Ollama installed and a local model matching `OLLAMA_MODEL`.
-	src/rag.py — The RAG runner. Glues retrieval, prompt building and the LLM together. Provides an interactive CLI entrypoint: it retrieves top-K chunks, prints them, builds a prompt and asks the LLM for an answer.

What each module does (short)
- **config.py**: Loads `.env`, validates `MONGODB_URI`, creates `mongo_client`, `db`, and `chunks_col` used across modules.
- **store.py**: Seeds the MongoDB collection with demo chunks (clears previous docs first). Use for populating the KB.
- **retrieve.py**: Fetches all chunks from MongoDB, computes a toy embedding per chunk and the query, ranks by dot-product, and returns the top-K chunks and scores.
- **prompt.py**: Given a query and a list of retrieved chunks, builds a human-readable prompt instructing the model to use ONLY that context when answering.
- **local_llm.py**: Calls `ollama.generate()` with the prompt and returns the text response. It relies on the Ollama Python package and a running Ollama daemon with the configured model.
- **rag.py**: Interactive pipeline entrypoint. Uses `retrieve_top_k`, `build_prompt`, and `generate` to show retrieved context and produced answer.

Environment
- Create a `.env` file in the repository root (not committed) with values like:

  MONGODB_URI=your_mongodb_connection_string
  OLLAMA_MODEL=llama3.1
  DB_NAME=rag_db
  COLLECTION_NAME=chunks

- `MONGODB_URI` is required. `OLLAMA_MODEL`, `DB_NAME`, and `COLLECTION_NAME` have defaults in `config.py`.

Setup
1. Create and activate a Python virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

3. Ensure Ollama is installed and a local model matching `OLLAMA_MODEL` is available. Start Ollama if needed (see Ollama docs).

4. Populate the knowledge base with demo chunks:

```bash
python src/store.py
```

Running the demo
- Run the interactive RAG CLI:

```bash
python src/rag.py
```

Type a question at the prompt. The program will:
- Retrieve the top-K chunks for your question (default K=3)
- Print the retrieved context and similarity scores
- Build a prompt that includes only the retrieved context
- Call the local LLM and print the generated answer

Notes and caveats
- Retriever: `retrieve.py` uses a simplistic, illustrative hash-based embedding. Replace with a vector model or external embedding service for real systems.
- LLM: `local_llm.py` uses the `ollama` package. The behavior depends on your local Ollama model and its configuration. Model loading may take time the first run.
- Security: This demo does not enforce access control or sanitize retrieved content against prompt injection. Do not use as-is in production.

Next steps / improvements
- Swap the toy embedding for OpenAI/Ada/E5 embeddings or a vector DB.
- Add paging or chunk overlap strategies for long documents.
- Add unit tests for retrieval and prompt formatting.
- Add graceful error handling when Ollama or MongoDB are unavailable.

License & attribution
- This is a small demo meant for learning and interviews; treat it as sample code.


