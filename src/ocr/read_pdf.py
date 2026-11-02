from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered
from pymongo import MongoClient
from bson import Binary

import tempfile
from src.config import MONGO_URI,MONGO_BDD,MONGO_COLLECTION_DOC,MONGO_COLLECTION_IMAGES,MONGO_COLLECTION_MD,MONGO_COLLECTION_METADATA_MD
from src.mongo.get_document_by_id import get_document_by_id,iter_document_content
from src.mongo.build_file_doc import build_file_doc

import io
import tempfile
import os
from datetime import datetime, timezone

_converter = None

def get_converter():
    global _converter
    if _converter is None:
        _converter = PdfConverter(artifact_dict=create_model_dict())
    return _converter


def image_to_png_bytes(image):
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def read_pdf(doc_id):
    client = MongoClient(MONGO_URI)
    try:
        db = client[MONGO_BDD]
        doc = get_document_by_id(doc_id, db, MONGO_COLLECTION_DOC)
        stem = os.path.splitext(doc["name"])[0] #nom du fichier sans extension

        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            for chunk in iter_document_content(doc, db):
                tmp.write(chunk)
            tmp.flush()
            rendered = get_converter()(tmp.name)

        text, meta_json, images = text_from_rendered(rendered)
        now = datetime.now(timezone.utc)

        text_id = db[MONGO_COLLECTION_MD].insert_one(
            build_file_doc(f"{stem}.md", text,"text/markdown", doc[id])
        ).inserted_id

        meta_id = db[MONGO_COLLECTION_METADATA_MD].insert_one(
            build_file_doc(f"{stem}_metadata.json", meta_json, "application/json", doc["_id"])
        ).inserted_id

        image_ids = []
        for name, image in images.items():
            png_name = os.path.splitext(name)[0] + ".png"
            res = db[MONGO_COLLECTION_IMAGES].insert_one(
                build_file_doc(png_name, image_to_png_bytes(image), "image/png", doc["_id"])
            )
            image_ids.append(res.inserted_id)

        return text_id, meta_id, image_ids
    finally:
        client.close()