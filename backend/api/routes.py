import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from backend.models.schemas import ATSScore, BatchResult, KeywordAnalysis, ComparisonResult
from backend.services.parser import parse_resume, parse_jd, extract_text
from backend.services.scorer import calculate_ats_score
from backend.services.matcher import matcher
from backend.services.batch import run_batch, get_batch
from backend.services.reporter import generate_pdf_report
from backend.utils.file_handler import save_upload
from backend.utils.logger import logger
from collections import Counter

router = APIRouter(prefix="/api")

_store: dict[str, dict] = {}
_jd_store: dict[str, dict] = {}


@router.post("/upload/resume")
async def upload_resume(file: UploadFile = File(...)):
    filepath = await save_upload(file, "uploads")
    data = parse_resume(filepath)
    rid = str(uuid.uuid4())[:8]
    data["id"] = rid
    _store[rid] = data
    return {"id": rid, "filename": file.filename, "candidate_name": data["candidate_name"]}


@router.post("/upload/jd")
async def upload_jd(file: UploadFile = File(...)):
    filepath = await save_upload(file, "jd")
    data = parse_jd(filepath)
    jid = str(uuid.uuid4())[:8]
    data["id"] = jid
    _jd_store[jid] = data
    return {"id": jid, "filename": file.filename, "title": data["title"]}


@router.post("/score")
async def score_resume(resume_id: str = Form(...), jd_id: str = Form(...)):
    resume = _store.get(resume_id)
    jd = _jd_store.get(jd_id)
    if not resume or not jd:
        raise HTTPException(404, "Resume or JD not found")
    score = calculate_ats_score(
        resume_text=resume["raw_text"],
        jd_text=jd["raw_text"],
        resume_id=resume_id,
        candidate_name=resume["candidate_name"],
    )
    return score


@router.post("/score/direct")
async def score_direct(
    resume_text: str = Form(...),
    jd_text: str = Form(...),
    candidate_name: str = Form("Candidate"),
):
    rid = str(uuid.uuid4())[:8]
    score = calculate_ats_score(
        resume_text=resume_text,
        jd_text=jd_text,
        resume_id=rid,
        candidate_name=candidate_name,
    )
    return score


@router.post("/compare")
async def compare_resumes(
    resume_id_a: str = Form(...),
    resume_id_b: str = Form(...),
    jd_id: str = Form(...),
):
    jd = _jd_store.get(jd_id)
    if not jd:
        raise HTTPException(404, "JD not found")
    r_a = _store.get(resume_id_a)
    r_b = _store.get(resume_id_b)
    if not r_a or not r_b:
        raise HTTPException(404, "Resume not found")

    score_a = calculate_ats_score(r_a["raw_text"], jd["raw_text"], resume_id_a, r_a["candidate_name"])
    score_b = calculate_ats_score(r_b["raw_text"], jd["raw_text"], resume_id_b, r_b["candidate_name"])

    return ComparisonResult(
        resume_a=score_a,
        resume_b=score_b,
        differences={
            "overall_diff": round(score_a.overall_score - score_b.overall_score, 1),
            "skills_diff": sorted(set(score_a.matched_skills) - set(score_b.matched_skills)),
            "missing_diff": sorted(set(score_a.missing_skills) - set(score_b.missing_skills)),
        },
    )


@router.post("/batch")
async def batch_score(jd_id: str = Form(...)):
    jd = _jd_store.get(jd_id)
    if not jd:
        raise HTTPException(404, "JD not found")
    if not _store:
        raise HTTPException(400, "No resumes uploaded")

    job_id = str(uuid.uuid4())[:8]
    results = []
    failed = 0
    for rid, resume in _store.items():
        try:
            score = calculate_ats_score(
                resume_text=resume["raw_text"],
                jd_text=jd["raw_text"],
                resume_id=rid,
                candidate_name=resume["candidate_name"],
            )
            results.append(score)
        except Exception as e:
            logger.error("Batch scoring failed for %s: %s", rid, e)
            failed += 1

    return BatchResult(
        job_id=job_id,
        total=len(_store),
        completed=len(results),
        failed=failed,
        results=results,
        status="completed",
    )


@router.get("/batch/{job_id}")
async def batch_status(job_id: str):
    result = get_batch(job_id)
    if not result:
        raise HTTPException(404, "Batch not found")
    return result


@router.get("/rankings")
async def get_rankings(jd_id: str = ""):
    q = _jd_store.get(jd_id, {}).get("raw_text", "") if jd_id else ""
    if not q:
        return {"rankings": [], "total_candidates": 0}
    results = matcher.search(q, k=50)
    return {"rankings": results, "total_candidates": len(results)}


@router.get("/keyword-analysis")
async def keyword_analysis(resume_id: str, jd_id: str = ""):
    resume = _store.get(resume_id)
    if not resume:
        raise HTTPException(404, "Resume not found")
    jd_text = _jd_store.get(jd_id, {}).get("raw_text", "") if jd_id else ""

    resume_words = resume["raw_text"].lower().split()
    jd_words = jd_text.lower().split() if jd_text else []

    resume_counter = Counter(resume_words)
    jd_counter = Counter(jd_words)

    common = set(resume_counter.keys()) & set(jd_counter.keys()) if jd_counter else set(resume_counter.keys())
    return [
        KeywordAnalysis(
            keyword=w,
            frequency=resume_counter[w],
            category="technical" if len(w) > 5 else "general",
            is_present=w in jd_counter if jd_counter else True,
        )
        for w in sorted(common, key=lambda w: resume_counter[w], reverse=True)[:50]
    ]


@router.get("/resumes")
async def list_resumes():
    return [{"id": k, "filename": v.get("filename", ""), "candidate_name": v.get("candidate_name", "")} for k, v in _store.items()]


@router.get("/jds")
async def list_jds():
    return [{"id": k, "filename": v.get("filename", ""), "title": v.get("title", "")} for k, v in _jd_store.items()]


@router.get("/resume/{resume_id}")
async def get_resume(resume_id: str):
    r = _store.get(resume_id)
    if not r:
        raise HTTPException(404)
    return r


@router.get("/jd/{jd_id}")
async def get_jd(jd_id: str):
    j = _jd_store.get(jd_id)
    if not j:
        raise HTTPException(404)
    return j


@router.post("/report")
async def generate_report(resume_id: str = Form(...), jd_id: str = Form(...)):
    resume = _store.get(resume_id)
    jd = _jd_store.get(jd_id)
    if not resume or not jd:
        raise HTTPException(404, "Resume or JD not found")
    score = calculate_ats_score(resume["raw_text"], jd["raw_text"], resume_id, resume["candidate_name"])
    pdf_path = generate_pdf_report(score.model_dump())
    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=pdf_path.name,
    )


@router.delete("/clear")
async def clear_all():
    _store.clear()
    _jd_store.clear()
    matcher.clear()
    return {"status": "cleared"}
