import requests
import streamlit as st

API_BASE = "http://localhost:8000/api"


def _get_headers():
    return {}


def upload_file(endpoint: str, file) -> dict:
    url = f"{API_BASE}/{endpoint}"
    resp = requests.post(url, files={"file": file}, headers=_get_headers())
    resp.raise_for_status()
    # Invalidate cache
    list_resumes.clear()
    list_jds.clear()
    get_rankings.clear()
    return resp.json()


def upload_resume(file) -> dict:
    return upload_file("upload/resume", file)


def upload_jd(file) -> dict:
    return upload_file("upload/jd", file)


def score_resume(resume_id: str, jd_id: str) -> dict:
    resp = requests.post(
        f"{API_BASE}/score",
        data={"resume_id": resume_id, "jd_id": jd_id},
        headers=_get_headers(),
    )
    resp.raise_for_status()
    get_rankings.clear()
    return resp.json()


def score_direct(resume_text: str, jd_text: str, candidate: str = "Candidate") -> dict:
    resp = requests.post(
        f"{API_BASE}/score/direct",
        data={"resume_text": resume_text, "jd_text": jd_text, "candidate_name": candidate},
        headers=_get_headers(),
    )
    resp.raise_for_status()
    get_rankings.clear()
    return resp.json()


def compare_resumes(rid_a: str, rid_b: str, jid: str) -> dict:
    resp = requests.post(
        f"{API_BASE}/compare",
        data={"resume_id_a": rid_a, "resume_id_b": rid_b, "jd_id": jid},
        headers=_get_headers(),
    )
    resp.raise_for_status()
    return resp.json()


def start_batch(jd_id: str) -> dict:
    resp = requests.post(
        f"{API_BASE}/batch",
        data={"jd_id": jd_id},
        headers=_get_headers(),
    )
    resp.raise_for_status()
    return resp.json()


def get_batch_status(job_id: str) -> dict:
    resp = requests.get(f"{API_BASE}/batch/{job_id}", headers=_get_headers())
    resp.raise_for_status()
    return resp.json()


@st.cache_data
def get_rankings(jd_id: str) -> dict:
    resp = requests.get(f"{API_BASE}/rankings", params={"jd_id": jd_id}, headers=_get_headers())
    resp.raise_for_status()
    return resp.json()


@st.cache_data
def get_keyword_analysis(resume_id: str, jd_id: str = "") -> list:
    resp = requests.get(
        f"{API_BASE}/keyword-analysis",
        params={"resume_id": resume_id, "jd_id": jd_id},
        headers=_get_headers(),
    )
    resp.raise_for_status()
    return resp.json()


@st.cache_data
def list_resumes() -> list[dict]:
    resp = requests.get(f"{API_BASE}/resumes", headers=_get_headers())
    resp.raise_for_status()
    return resp.json()


@st.cache_data
def list_jds() -> list[dict]:
    resp = requests.get(f"{API_BASE}/jds", headers=_get_headers())
    resp.raise_for_status()
    return resp.json()


@st.cache_data
def get_resume(rid: str) -> dict:
    resp = requests.get(f"{API_BASE}/resume/{rid}", headers=_get_headers())
    resp.raise_for_status()
    return resp.json()


@st.cache_data
def get_jd(jid: str) -> dict:
    resp = requests.get(f"{API_BASE}/jd/{jid}", headers=_get_headers())
    resp.raise_for_status()
    return resp.json()


def download_report(resume_id: str, jd_id: str) -> bytes:
    resp = requests.post(
        f"{API_BASE}/report",
        data={"resume_id": resume_id, "jd_id": jd_id},
        headers=_get_headers(),
    )
    resp.raise_for_status()
    return resp.content


def clear_all():
    requests.delete(f"{API_BASE}/clear", headers=_get_headers())
    list_resumes.clear()
    list_jds.clear()
    get_rankings.clear()
    get_resume.clear()
    get_jd.clear()
    get_keyword_analysis.clear()



def health_check() -> bool:
    try:
        resp = requests.get(f"{API_BASE.replace('/api', '')}/health", timeout=3)
        return resp.ok
    except:
        return False
