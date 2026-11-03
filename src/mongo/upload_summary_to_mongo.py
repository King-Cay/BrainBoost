from pymongo import MongoClient
from datetime import datetime
import os
from src.mongo.build_file_doc import build_file_doc
from src.config import MONGO_URI, MONGO_BDD, MONGO_COLLECTION_DOC

def upload_resume_to_mongo(summary_text, source_doc, model_used, db, collection, ratio=None):
    """
    Insère le résumé d'un document dans MongoDB.

    Args:
        summary_text (str): le résumé généré.
        source_doc (dict): le document PDF d'origine (avec "_id" et "name").
        model_used (str): modèle utilisé pour générer le résumé.
        db (Database): la base MongoDB.
        collection (str): la collection de destination.
        ratio (float, optionnel): taux de compression demandé.

    Returns:
        ObjectId: l'id du document de résumé.
    """
    stem = os.path.splitext(source_doc["name"])[0]
    doc = build_file_doc(
        f"{stem}_summary.md",
        summary_text,
        "text/markdown",
        source_doc["_id"],
        kind="summary",
        model_used=model_used,
        ratio=ratio,
    )
    res = db[collection].replace_one(
        {"source_id": source_doc["_id"], "kind": "summary", "model_used": model_used},
        doc,
        upsert=True,
    )
    return res.upserted_id or db[collection].find_one(
        {"source_id": source_doc["_id"], "kind": "summary", "model_used": model_used},
        {"_id": 1},
    )["_id"]