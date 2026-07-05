import re
from pathlib import Path
import PyPDF2
import docx
from backend.utils.logger import logger


def extract_text(filepath: Path) -> str:
    ext = filepath.suffix.lower()
    if ext == ".pdf":
        return _extract_pdf(filepath)
    elif ext == ".docx":
        return _extract_docx(filepath)
    elif ext == ".txt":
        return filepath.read_text(encoding="utf-8")
    return ""


def _extract_pdf(filepath: Path) -> str:
    text = []
    with open(filepath, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text.append(t)
    return "\n".join(text)


def _extract_docx(filepath: Path) -> str:
    doc = docx.Document(filepath)
    return "\n".join(p.text for p in doc.paragraphs)


def parse_resume(filepath: Path) -> dict:
    raw = extract_text(filepath)
    data = {
        "filename": filepath.name,
        "raw_text": raw,
        "candidate_name": _extract_name(raw),
        "email": _extract_email(raw),
        "phone": _extract_phone(raw),
        "skills": _extract_skills(raw),
        "experience": _extract_experience(raw),
        "education": _extract_education(raw),
    }
    logger.info("Parsed resume: %s", filepath.name)
    return data


def parse_jd(filepath: Path) -> dict:
    raw = extract_text(filepath)
    data = {
        "filename": filepath.name,
        "raw_text": raw,
        "title": _extract_jd_title(raw),
        "required_skills": _extract_skills(raw),
        "preferred_skills": [],
        "responsibilities": [],
        "qualifications": [],
    }
    logger.info("Parsed JD: %s", filepath.name)
    return data


SKILL_KB = {
    "python", "java", "javascript", "typescript", "go", "rust", "c++", "c#",
    "react", "angular", "vue", "node.js", "node", "express", "django", "flask",
    "fastapi", "spring", "sql", "nosql", "postgresql", "mysql", "mongodb",
    "redis", "docker", "kubernetes", "aws", "gcp", "azure", "ci/cd", "git",
    "machine learning", "deep learning", "nlp", "computer vision", "tensorflow",
    "pytorch", "scikit-learn", "pandas", "numpy", "data analysis", "data science",
    "tableau", "power bi", "excel", "agile", "scrum", "jira", "rest api",
    "graphql", "grpc", "kafka", "rabbitmq", "terraform", "ansible",
    "linux", "bash", "powershell", "html", "css", "sass", "tailwind",
    "redux", "next.js", "nuxt.js", "flutter", "react native", "swift",
    "kotlin", "oop", "microservices", "serverless", "blockchain",
    "devops", "mlops", "data pipeline", "etl", "airflow", "spark",
    "hadoop", "elasticsearch", "logstash", "kibana", "prometheus",
    "grafana", "jenkins", "github actions", "gitlab ci", "circleci",
    "nginx", "apache", "iis", "load balancing", "caching", "varnish",
}


def _extract_name(text: str) -> str:
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    return lines[0] if lines else ""


def _extract_email(text: str) -> str:
    m = re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", text)
    return m.group(0) if m else ""


def _extract_phone(text: str) -> str:
    m = re.search(r"[\+\(]?[\d\s\-\.\(\)]{7,}", text)
    return m.group(0).strip() if m else ""


def _extract_skills(text: str) -> list[str]:
    lower = text.lower()
    found = set()
    for skill in SKILL_KB:
        pattern = re.compile(r"\b" + re.escape(skill) + r"\b", re.IGNORECASE)
        if pattern.search(lower):
            found.add(skill)
    return sorted(found)


def _extract_experience(text: str) -> list[dict]:
    entries = []
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if re.search(r"(experience|work|employment|job)\s*:?\s*$", line, re.I):
            for l in lines[i + 1 : i + 10]:
                l = l.strip()
                if not l or re.search(r"(education|skills|projects)\s*:?\s*$", l, re.I):
                    break
                if l:
                    entries.append({"description": l})
    return entries


def _extract_education(text: str) -> list[dict]:
    entries = []
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if re.search(r"(education|academic|qualification)\s*:?\s*$", line, re.I):
            for l in lines[i + 1 : i + 8]:
                l = l.strip()
                if not l or re.search(r"(experience|skills|projects)\s*:?\s*$", l, re.I):
                    break
                if l:
                    entries.append({"description": l})
    return entries


def _extract_jd_title(text: str) -> str:
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    return lines[0] if lines else ""
