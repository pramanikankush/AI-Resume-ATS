import json
import numpy as np
from pathlib import Path
from backend.core.config import settings
from backend.services.embeddings import embed_text, embed_batch
from backend.utils.logger import logger

# Try importing faiss, fallback to NumPy if not available (e.g. on Vercel due to missing libgomp)
try:
    import faiss
    HAS_FAISS = True
except ImportError:
    logger.warning("FAISS not available. Falling back to NumPy-based similarity matching.")
    HAS_FAISS = False


class FAISSMatcher:
    def __init__(self):
        self.index = None       # For FAISS
        self.vectors = None     # For NumPy fallback
        self.metadata = []
        self.dim = 384
        self._load()

    def _load(self):
        # Load metadata
        if settings.FAISS_METADATA_PATH.exists():
            try:
                self.metadata = json.loads(
                    settings.FAISS_METADATA_PATH.read_text()
                )
            except Exception as e:
                logger.error("Failed to load metadata: %s", e)

        # Load vectors
        if HAS_FAISS:
            if settings.FAISS_INDEX_PATH.exists():
                try:
                    self.index = faiss.read_index(str(settings.FAISS_INDEX_PATH))
                    logger.info("Loaded FAISS index with %d entries", len(self.metadata))
                    return
                except Exception as e:
                    logger.error("Failed to load FAISS index: %s", e)
        
        # NumPy Fallback loading
        npy_path = Path(str(settings.FAISS_INDEX_PATH).replace(".index", ".npy"))
        if npy_path.exists():
            try:
                self.vectors = np.load(str(npy_path))
                logger.info("Loaded NumPy vectors with %d entries", len(self.metadata))
            except Exception as e:
                logger.error("Failed to load NumPy vectors: %s", e)

    def _save(self):
        # Save metadata
        try:
            settings.FAISS_METADATA_PATH.write_text(json.dumps(self.metadata))
        except Exception as e:
            logger.error("Failed to save metadata: %s", e)

        # Save vectors
        if HAS_FAISS and self.index is not None:
            try:
                faiss.write_index(self.index, str(settings.FAISS_INDEX_PATH))
                logger.info("Saved FAISS index with %d entries", len(self.metadata))
            except Exception as e:
                logger.error("Failed to save FAISS index: %s", e)
        
        if self.vectors is not None:
            try:
                npy_path = Path(str(settings.FAISS_INDEX_PATH).replace(".index", ".npy"))
                np.save(str(npy_path), self.vectors)
                logger.info("Saved NumPy vectors with %d entries", len(self.metadata))
            except Exception as e:
                logger.error("Failed to save NumPy vectors: %s", e)

    def add_resume(self, resume_id: str, text: str, metadata: dict):
        vec = np.array([embed_text(text)], dtype=np.float32)
        
        # FAISS path
        if HAS_FAISS:
            if self.index is None:
                self.index = faiss.IndexFlatIP(self.dim)
            self.index.add(vec)

        # NumPy path
        if self.vectors is None:
            self.vectors = vec
        else:
            self.vectors = np.vstack([self.vectors, vec])

        self.metadata.append({"resume_id": resume_id, **metadata})
        self._save()

    def add_batch(self, ids: list[str], texts: list[str], metadatas: list[dict]):
        vecs = np.array(embed_batch(texts), dtype=np.float32)
        
        # FAISS path
        if HAS_FAISS:
            if self.index is None:
                self.index = faiss.IndexFlatIP(self.dim)
            self.index.add(vecs)

        # NumPy path
        if self.vectors is None:
            self.vectors = vecs
        else:
            self.vectors = np.vstack([self.vectors, vecs])

        for rid, m in zip(ids, metadatas):
            self.metadata.append({"resume_id": rid, **m})
        self._save()

    def search(self, query: str, k: int = 10) -> list[dict]:
        if len(self.metadata) == 0:
            return []

        vec = np.array([embed_text(query)], dtype=np.float32)
        
        # If FAISS is active and loaded
        if HAS_FAISS and self.index is not None and self.index.ntotal > 0:
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

        # NumPy search path (Inner Product/Cosine Similarity matching)
        if self.vectors is None or len(self.vectors) == 0:
            return []
        
        sims = np.dot(self.vectors, vec.T).flatten()
        
        results = []
        for idx, score in enumerate(sims):
            if idx < len(self.metadata):
                results.append({
                    "resume_id": self.metadata[idx]["resume_id"],
                    "score": float(score),
                    "candidate_name": self.metadata[idx].get("candidate_name", ""),
                })
        
        sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
        return sorted_results[:k]

    def semantic_similarity(self, text_a: str, text_b: str) -> float:
        vec_a = np.array([embed_text(text_a)], dtype=np.float32)
        vec_b = np.array([embed_text(text_b)], dtype=np.float32)
        sim = np.dot(vec_a, vec_b.T)[0][0]
        return float(max(0, min(1, (sim + 1) / 2)))

    def clear(self):
        self.index = None
        self.vectors = None
        self.metadata = []
        if settings.FAISS_INDEX_PATH.exists():
            settings.FAISS_INDEX_PATH.unlink()
        if settings.FAISS_METADATA_PATH.exists():
            settings.FAISS_METADATA_PATH.unlink()
            
        npy_path = Path(str(settings.FAISS_INDEX_PATH).replace(".index", ".npy"))
        if npy_path.exists():
            npy_path.unlink()


matcher = FAISSMatcher()
