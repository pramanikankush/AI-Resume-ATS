from pathlib import Path
from fastapi import UploadFile
from backend.core.config import settings
from backend.utils.logger import logger


ALLOWED = {".pdf", ".docx", ".txt"}


async def save_upload(file: UploadFile, subdir: str = "uploads") -> Path:
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED:
        raise ValueError(f"Unsupported file type: {ext}")
    dest = settings.UPLOAD_DIR.parent / subdir / file.filename
    dest.parent.mkdir(parents=True, exist_ok=True)
    content = await file.read()
    if len(content) > settings.MAX_UPLOAD_SIZE:
        raise ValueError("File too large")
    dest.write_bytes(content)
    logger.info("Saved %s (%d bytes)", dest.name, len(content))
    return dest
