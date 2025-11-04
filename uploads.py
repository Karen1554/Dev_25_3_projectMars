import os
import uuid
from pathlib import Path
from fastapi import UploadFile



STORE_DIR = "uploads"

Path(STORE_DIR).mkdir(parents=True, exist_ok=True)

async def upload_file(file: UploadFile):
    content = await file.read()
    filename_org=file.filename
    ##file_ext = Path(file.filename).suffix
    filename = f"{uuid.uuid4()}_{filename_org}"

    file_path = os.path.join(STORE_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(content)

    return {
        "filename": filename,
        "original_filename": file.filename,
        "path": file_path,
        "size": os.path.getsize(file_path),
        "url":f"/img/{filename}",
    }

