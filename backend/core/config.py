import os
from pathlib import Path


class Settings:
    APP_NAME: str = "AI Resume Screening ATS"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    IS_VERCEL: bool = os.getenv("VERCEL") is not None
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    
    # Use /tmp on Vercel since the rest of the filesystem is read-only
    DATA_DIR: Path = Path("/tmp") if IS_VERCEL else BASE_DIR

    UPLOAD_DIR: Path = DATA_DIR / "data" / "uploads"
    REPORT_DIR: Path = DATA_DIR / "data" / "reports"
    FAISS_DIR: Path = DATA_DIR / "data" / "faiss_index"
    LOG_DIR: Path = DATA_DIR / "logs"

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    FAISS_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024
    ALLOWED_EXTENSIONS: set = {".pdf", ".docx", ".txt"}

    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    SENTENCE_TRANSFORMER_MODEL: str = os.getenv(
        "SENTENCE_TRANSFORMER_MODEL",
        "all-MiniLM-L6-v2",
    )
    FAISS_INDEX_PATH: Path = FAISS_DIR / "resumes.index"
    FAISS_METADATA_PATH: Path = FAISS_DIR / "metadata.json"

    ATS_WEIGHTS: dict = {
        "keyword_match": 0.30,
        "semantic_match": 0.30,
        "skills_coverage": 0.20,
        "experience_relevance": 0.10,
        "education_match": 0.10,
    }


settings = Settings()
