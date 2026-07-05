from datetime import datetime
from pydantic import BaseModel


class ResumeBase(BaseModel):
    filename: str
    candidate_name: str = ""
    email: str = ""
    phone: str = ""
    skills: list[str] = []
    experience: list[dict] = []
    education: list[dict] = []
    raw_text: str = ""


class ResumeParsed(ResumeBase):
    id: str
    uploaded_at: datetime = datetime.now()


class JobDescription(BaseModel):
    id: str
    title: str = ""
    company: str = ""
    required_skills: list[str] = []
    preferred_skills: list[str] = []
    responsibilities: list[str] = []
    qualifications: list[str] = []
    raw_text: str = ""
    uploaded_at: datetime = datetime.now()


class ATSScore(BaseModel):
    resume_id: str
    candidate_name: str
    overall_score: float
    keyword_match: float
    semantic_match: float
    skills_coverage: float
    experience_relevance: float
    education_match: float
    matched_skills: list[str]
    missing_skills: list[str]
    recommendations: list[str]


class CandidateRanking(BaseModel):
    rankings: list[ATSScore]
    total_candidates: int


class ComparisonResult(BaseModel):
    resume_a: ATSScore
    resume_b: ATSScore
    differences: dict


class BatchResult(BaseModel):
    job_id: str
    total: int
    completed: int
    failed: int
    results: list[ATSScore]
    status: str
    created_at: datetime = datetime.now()


class KeywordAnalysis(BaseModel):
    keyword: str
    frequency: int
    category: str
    is_present: bool


class ReportRequest(BaseModel):
    resume_ids: list[str]
    format: str = "pdf"
