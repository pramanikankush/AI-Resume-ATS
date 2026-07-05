from backend.core.config import settings
from backend.models.schemas import ATSScore
from backend.services.llm import analyze_resume
from backend.services.matcher import matcher
from backend.utils.logger import logger


def calculate_ats_score(
    resume_text: str,
    jd_text: str,
    resume_id: str,
    candidate_name: str,
) -> ATSScore:
    llm_result = analyze_resume(resume_text, jd_text)
    semantic = matcher.semantic_similarity(resume_text, jd_text) * 100

    kw_score = llm_result.get("keyword_match", 50)
    sk_score = llm_result.get("skills_coverage", 50)
    ex_score = llm_result.get("experience_relevance", 50)
    ed_score = llm_result.get("education_match", 50)

    w = settings.ATS_WEIGHTS
    overall = (
        kw_score * w["keyword_match"]
        + semantic * w["semantic_match"]
        + sk_score * w["skills_coverage"]
        + ex_score * w["experience_relevance"]
        + ed_score * w["education_match"]
    )

    score = ATSScore(
        resume_id=resume_id,
        candidate_name=candidate_name,
        overall_score=round(overall, 1),
        keyword_match=round(kw_score, 1),
        semantic_match=round(semantic, 1),
        skills_coverage=round(sk_score, 1),
        experience_relevance=round(ex_score, 1),
        education_match=round(ed_score, 1),
        matched_skills=llm_result.get("matched_skills", []),
        missing_skills=llm_result.get("missing_skills", []),
        recommendations=llm_result.get("recommendations", []),
    )

    matcher.add_resume(resume_id, resume_text, {"candidate_name": candidate_name})
    logger.info("ATS score for %s: %.1f", candidate_name, overall)
    return score
