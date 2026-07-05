import asyncio
import uuid
from datetime import datetime
from backend.core.config import settings
from backend.models.schemas import ATSScore, BatchResult
from backend.services.parser import parse_resume, parse_jd
from backend.services.scorer import calculate_ats_score
from backend.utils.logger import logger


_jobs: dict[str, BatchResult] = {}


async def run_batch(
    resume_paths: list,
    jd_text: str,
    jd_id: str,
) -> BatchResult:
    job_id = str(uuid.uuid4())[:8]
    result = BatchResult(
        job_id=job_id,
        total=len(resume_paths),
        completed=0,
        failed=0,
        results=[],
        status="running",
    )
    _jobs[job_id] = result
    logger.info("Batch %s started: %d resumes", job_id, len(resume_paths))

    for rp in resume_paths:
        try:
            resume_data = parse_resume(rp)
            score = calculate_ats_score(
                resume_text=resume_data["raw_text"],
                jd_text=jd_text,
                resume_id=str(uuid.uuid4())[:8],
                candidate_name=resume_data["candidate_name"],
            )
            result.results.append(score)
            result.completed += 1
            await asyncio.sleep(0.1)
        except Exception as e:
            logger.error("Batch %s failed for %s: %s", job_id, rp.name, e)
            result.failed += 1

    result.status = "completed"
    _jobs[job_id] = result
    logger.info("Batch %s done: %d ok, %d failed", job_id, result.completed, result.failed)
    return result


def get_batch(job_id: str) -> BatchResult | None:
    return _jobs.get(job_id)
