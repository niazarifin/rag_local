"""
Use this script to test your connection to MongoDB Atlas.
"""

# src/ping.py

import certifi
from pymongo import MongoClient

# MONGODB_URI = "YOUR_MONGODB_URI_HERE"  # keep mongodb+srv:// if using Atlas
MONGODB_URI="mongodb+srv://arifin_db_user:fQXYZfkFVdbLlvp9@arif-cluster.zs0vufz.mongodb.net/?appName=arif-Cluster"

def main():
    client = MongoClient(
        MONGODB_URI,
        tls=True,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=30000,
    )
    print(client.admin.command("ping"))

if __name__ == "__main__":
    main()
