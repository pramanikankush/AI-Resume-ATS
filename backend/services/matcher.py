import json
import numpy as np
import faiss
from pathlib import Path
from backend.core.config import settings
from backend.services.embeddings import embed_text, embed_batch
from backend.utils.logger import logger


class FAISSMatcher:
    def __init__(self):
        self.index = None
        self.metadata = []
        self.dim = 384
        self._load()

    def _load(self):
        if settings.FAISS_INDEX_PATH.exists():
            try:
                self.index = faiss.read_index(str(settings.FAISS_INDEX_PATH))
                if settings.FAISS_METADATA_PATH.exists():
                    self.metadata = json.loads(
                        settings.FAISS_METADATA_PATH.read_text()
                    )
                logger.info("Loaded FAISS index with %d entries", len(self.metadata))
            except Exception as e:
                logger.error("Failed to load FAISS index: %s", e)

    def _save(self):
        if self.index is not None:
            faiss.write_index(self.index, str(settings.FAISS_INDEX_PATH))
            settings.FAISS_METADATA_PATH.write_text(json.dumps(self.metadata))
            logger.info("Saved FAISS index with %d entries", len(self.metadata))

    def add_resume(self, resume_id: str, text: str, metadata: dict):
        vec = np.array([embed_text(text)], dtype=np.float32)
        if self.index is None:
            self.index = faiss.IndexFlatIP(self.dim)
        self.index.add(vec)
        self.metadata.append({"resume_id": resume_id, **metadata})
        self._save()

    def add_batch(self, ids: list[str], texts: list[str], metadatas: list[dict]):
        vecs = np.array(embed_batch(texts), dtype=np.float32)
        if self.index is None:
            self.index = faiss.IndexFlatIP(self.dim)
        self.index.add(vecs)
        for rid, m in zip(ids, metadatas):
            self.metadata.append({"resume_id": rid, **m})
        self._save()

    def search(self, query: str, k: int = 10) -> list[dict]:
        if self.index is None or self.index.ntotal == 0:
            return []
        vec = np.array([embed_text(query)], dtype=np.float32)
        scores, indices = self.index.search(vec, min(k, self.index.ntotal))
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.metadata):
                results.append({
                    "resume_id": self.metadata[idx]["resume_id"],
                    "score": float(score),
                    "candidate_name": self.metadata[idx].get("candidate_name", ""),
                })
        return sorted(results, key=lambda x: x["score"], reverse=True)

    def semantic_similarity(self, text_a: str, text_b: str) -> float:
        vec_a = np.array([embed_text(text_a)], dtype=np.float32)
        vec_b = np.array([embed_text(text_b)], dtype=np.float32)
        sim = np.dot(vec_a, vec_b.T)[0][0]
        return float(max(0, min(1, (sim + 1) / 2)))

    def clear(self):
        self.index = None
        self.metadata = []
        if settings.FAISS_INDEX_PATH.exists():
            settings.FAISS_INDEX_PATH.unlink()
        if settings.FAISS_METADATA_PATH.exists():
            settings.FAISS_METADATA_PATH.unlink()


matcher = FAISSMatcher()
