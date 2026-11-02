from pymongo import MongoClient
import os
from src.config import MONGO_URI, MONGO_BDD

def get_all_id_from_collection(collection):
    client = MongoClient(MONGO_URI)
    try:
        col = client[MONGO_BDD][collection]
        return [doc["_id"] for doc in col.find({}, {"_id": 1})]
    finally:
        client.close()


