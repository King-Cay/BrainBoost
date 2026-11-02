import os
from datetime import datetime, timezone
from bson import Binary


def build_file_doc(name, content, mime, source_id=None):
    if isinstance(content, str):
        storage, stored, size = "text", content, len(content.encode("utf-8"))
    else:
        storage, stored, size = "binary", Binary(content), len(content)

    doc = {
        "name": name,
        "extension": os.path.splitext(name)[1][1:].lower(),
        "type": mime,
        "size": size,
        "storage": storage,
        "content": stored,
        "added_at": datetime.now(timezone.utc),
    }
    if source_id is not None:
        doc["source_id"] = source_id
    return doc