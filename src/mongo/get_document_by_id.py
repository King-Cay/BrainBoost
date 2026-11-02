from bson import ObjectId
from bson.errors import InvalidId
import gridfs
import json

def get_document_by_id(doc_id,db,collection):

    try:
        oid = ObjectId(doc_id)
    except InvalidId:
        raise ValueError(f"Identifiant invalide : {doc_id!r}")

    doc = db[collection].find_one({
        "_id" : oid
    })

    if doc is None:
        raise FileNotFoundError(f"Aucun document avec l'id {doc_id!r}")

    return doc

def iter_document_content(doc, db):
    storage = doc["storage"]
    if storage == "binary":
        yield bytes(doc["content"])
    elif storage == "gridfs":
        yield from gridfs.GridFS(db).get(doc["gridfs_id"])
    elif storage == "text":
        yield doc["content"].encode("utf-8")
    else:
        raise ValueError(f"Type de stockage inconnu : {storage!r}")