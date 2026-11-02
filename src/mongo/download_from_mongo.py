from pymongo import MongoClient
import gridfs
import os
from src.config import MONGO_URI, MONGO_BDD, MONGO_COLLECTION_DOC ,OUTPUT_DIR
from src.mongo.get_document_by_id import get_document_by_id, iter_document_content


def download_from_mongo(doc_id,collection, output_dir=OUTPUT_DIR):
    client = MongoClient(MONGO_URI)
    try:
        db = client[MONGO_BDD]
        doc = get_document_by_id(doc_id, db, collection)

        name = os.path.basename(doc["name"])
        if "source_id" in doc:                 # fichier dérivé : préfixe pour éviter les collisions
            name = f"{doc['_id']}_{name}"

        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, name)
        tmp_path = path + ".part"

        try:
            with open(tmp_path, "wb") as f:
                for chunk in iter_document_content(doc,db):
                    f.write(chunk)
            os.replace(tmp_path, path)      # renommage atomique
        except Exception:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            raise

        return path
    finally:
        client.close()



if __name__ == "__main__" :
    path = download_from_mongo("6ae8643f1b41ef665d2c7320",MONGO_COLLECTION_DOC)
    print("fichier copié à "+path)