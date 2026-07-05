import numpy as np
from backend.core.config import settings
from backend.utils.logger import logger

_gemini_client = None
_st_model = None


def _get_gemini():
    global _gemini_client
    if _gemini_client is None and settings.GEMINI_API_KEY:
        try:
            import google.generativeai as genai
            genai.configure(api_key=settings.GEMINI_API_KEY)
            _gemini_client = genai
        except Exception as e:
            logger.warning("Gemini init failed: %s", e)
    return _gemini_client


def _get_st_model():
    global _st_model
    if _st_model is None:
        try:
            from sentence_transformers import SentenceTransformer
            _st_model = SentenceTransformer(settings.SENTENCE_TRANSFORMER_MODEL)
        except Exception as e:
            logger.error("SentenceTransformer load failed: %s", e)
            raise
    return _st_model


def embed_text(text: str) -> list[float]:
    gemini = _get_gemini()
    if gemini:
        try:
            result = gemini.embed_content(
                model="models/embedding-001",
                content=text,
                task_type="retrieval_document",
            )
            return result["embedding"]
        except Exception as e:
            logger.warning("Gemini embedding failed, falling back: %s", e)

    model = _get_st_model()
    vec = model.encode([text], normalize_embeddings=True)[0]
    return vec.tolist()


def embed_batch(texts: list[str]) -> list[list[float]]:
    gemini = _get_gemini()
    if gemini:
        try:
            results = gemini.embed_content(
                model="models/embedding-001",
                content=texts,
                task_type="retrieval_document",
            )
            return results["embedding"]
        except Exception as e:
            logger.warning("Gemini batch failed, falling back: %s", e)

    model = _get_st_model()
    vecs = model.encode(texts, normalize_embeddings=True)
    return vecs.tolist()
