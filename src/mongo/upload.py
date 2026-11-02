from pymongo import MongoClient
from bson.binary import Binary
import os
import mimetypes
import gridfs
from datetime import datetime
from src.config import MONGO_URI, MONGO_BDD, MONGO_COLLECTION, THRESHOLD


def get_metadata(filepath):
    name = os.path.basename(filepath)
    extension = os.path.splitext(name)[1][1:].lower()   # "pdf" (sans le point)
    mime, _ = mimetypes.guess_type(name)
    return {
        "name": name,
        "extension": extension,
        "type": mime or "application/octet-stream",
        "size": os.path.getsize(filepath),
    }


def upload_to_mongo_small(db, metadata, data):
    res = db[MONGO_COLLECTION].insert_one({
        **metadata,
        "storage": "binary",
        "added_at": datetime.now(),
        "content": Binary(data),
    })
    return res.inserted_id


def upload_to_mongo_big(db, metadata, fileobj):
    fs = gridfs.GridFS(db)
    file_id = fs.put(
        fileobj,
        filename=metadata["name"],
        content_type=metadata["type"],
        size=metadata["size"],
        extension=metadata["extension"],
    )
    # Document de référence dans la même collection que les petits fichiers
    res = db[MONGO_COLLECTION].insert_one({
        **metadata,
        "storage": "gridfs",
        "gridfs_id": file_id,
        "added_at": datetime.now(),
    })
    return res.inserted_id


def upload_to_mongo(filepath):
    metadata = get_metadata(filepath)

    client = MongoClient(MONGO_URI)
    try:
        db = client[MONGO_BDD]
        with open(filepath, "rb") as f:
            if metadata["size"] > THRESHOLD:
                return upload_to_mongo_big(db, metadata, f)
            return upload_to_mongo_small(db, metadata, f.read())
    finally:
        client.close()