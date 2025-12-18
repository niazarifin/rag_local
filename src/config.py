"""
Configuration for MongoDB connection and Ollama model.
Analogy: MongoDB opens a connection to the filing cabinet.
    - connects to MongoDB Atlas
    - selects a database
    - exposes chunks_col (my collection handle)
Loads environment variables from a .env file.
"""

import os
import certifi
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")
DB_NAME = os.getenv("DB_NAME", "rag_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "chunks")

if not MONGODB_URI:
    raise RuntimeError("Missing MONGODB_URI in .env")

mongo_client = MongoClient(
    MONGODB_URI,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=10000,
)
mongo_client.admin.command("ping")

db = mongo_client[DB_NAME]
chunks_col = db[COLLECTION_NAME]

if __name__ == "__main__":
    print("✅ Mongo ping:", mongo_client.admin.command("ping"))
    print("✅ DB:", DB_NAME, "| Collection:", COLLECTION_NAME)
    print("✅ Ollama model:", OLLAMA_MODEL)
