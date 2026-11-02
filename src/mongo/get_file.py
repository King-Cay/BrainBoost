from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId
import gridfs
import os
from src.config import MONGO_URI, MONGO_BDD, MONGO_COLLECTION ,OUTPUT_DIR


def download_from_mongo(doc_id,output_dir=OUTPUT_DIR):

    try:
        oid = ObjectId(doc_id)
    except InvalidId:
        raise ValueError(f"Identifiant invalide : {doc_id!r}")
    
    client = MongoClient(MONGO_URI)
    try:
        db = client[MONGO_BDD]
        doc = db[MONGO_COLLECTION].find_one({
            "_id" : oid
        })

        if doc is None:
            raise FileNotFoundError(f"Aucun document avec l'id {doc_id!r}")

        

        os.makedirs(output_dir,exist_ok=True)
        path = os.path.join(output_dir,doc["name"])
        with open(path,'wb') as f:
            if doc["storage"] == "binary":
                f.write(doc["content"])
            else:
                grid_out = gridfs.GridFS(db).get(doc["gridfs_id"])
                for chunk in grid_out :
                    f.write(chunk)
            return path
    finally:
        client.close()

if __name__ == "__main__" :
    path = download_from_mongo("6ae8643f1b41ef665d2c7320")
    print("fichier copié à "+path)