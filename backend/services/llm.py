import json
from backend.core.config import settings
from backend.utils.logger import logger

_client = None


def _get_client():
    global _client
    if _client is None and settings.GROQ_API_KEY:
        try:
            from groq import Groq
            _client = Groq(api_key=settings.GROQ_API_KEY)
        except Exception as e:
            logger.warning("Groq init failed: %s", e)
    return _client


def analyze_resume(resume_text: str, jd_text: str) -> dict:
    client = _get_client()
    if not client:
        return _local_analysis(resume_text, jd_text)

    prompt = f"""You are an ATS expert. Analyze this resume against the job description.

Job Description:
{jd_text[:2000]}

Resume:
{resume_text[:2000]}

Return JSON with:
- keyword_match (0-100): how well resume keywords match JD
- skills_coverage (0-100): what % of required skills are present
- experience_relevance (0-100): how relevant experience is
- education_match (0-100): education fit
- matched_skills: list of matched skills
- missing_skills: list of missing important skills
- recommendations: list of 3-5 improvement tips"""

    try:
        resp = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            response_format={"type": "json_object"},
        )
        return json.loads(resp.choices[0].message.content)
    except Exception as e:
        logger.error("Groq API error: %s", e)
        return _local_analysis(resume_text, jd_text)


def _local_analysis(resume_text: str, jd_text: str) -> dict:
    from backend.services.parser import _extract_skills, SKILL_KB
    resume_skills = set(_extract_skills(resume_text))
    jd_skills = set(_extract_skills(jd_text))

    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills
    coverage = len(matched) / max(len(jd_skills), 1) * 100

    return {
        "keyword_match": min(coverage * 1.2, 100),
        "skills_coverage": coverage,
        "experience_relevance": min(coverage * 0.8 + 20, 100),
        "education_match": 70.0,
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
        "recommendations": [
            f"Add missing skills: {', '.join(list(missing)[:5])}" if missing else "Good skill coverage",
            "Quantify experience with metrics",
            "Tailor summary to the job description",
        ],
    }


def generate_report_summary(score_data: dict) -> str:
    client = _get_client()
    if not client:
        return _local_summary(score_data)

    prompt = f"""Write a 2-paragraph ATS analysis summary for this candidate:
Score: {score_data.get('overall_score', 0)}/100
Matched: {score_data.get('matched_skills', [])}
Missing: {score_data.get('missing_skills', [])}
Make it professional and actionable."""

    try:
        resp = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        return resp.choices[0].message.content
    except Exception:
        return _local_summary(score_data)


def _local_summary(score_data: dict) -> str:
    score = score_data.get("overall_score", 0)
    matched = score_data.get("matched_skills", [])
    missing = score_data.get("missing_skills", [])

    if score >= 80:
        rating = "strong match"
    elif score >= 60:
        rating = "moderate match"
    else:
        rating = "weak match"

    return (
        f"Candidate scores {score:.0f}/100 — {rating}. "
        f"Matched {len(matched)} skills. "
        f"Missing {len(missing)} skills. "
        f"Recommend focusing on {' and '.join(missing[:3])}."
    )
