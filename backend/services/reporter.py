from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from backend.core.config import settings
from backend.utils.logger import logger


def generate_pdf_report(score_data: dict, output_path: Path = None) -> Path:
    if output_path is None:
        output_path = settings.REPORT_DIR / f"report_{score_data.get('resume_id', 'unknown')}.pdf"

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"ATS Resume Report", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"<b>Candidate:</b> {score_data.get('candidate_name', 'N/A')}", styles["Normal"]))
    story.append(Paragraph(f"<b>Overall Score:</b> {score_data.get('overall_score', 0)}/100", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Score Breakdown</b>", styles["Heading2"]))
    for key in ["keyword_match", "semantic_match", "skills_coverage", "experience_relevance", "education_match"]:
        label = key.replace("_", " ").title()
        val = score_data.get(key, 0)
        story.append(Paragraph(f"{label}: {val}/100", styles["Normal"]))

    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>Matched Skills</b>", styles["Heading2"]))
    matched = score_data.get("matched_skills", [])
    story.append(Paragraph(", ".join(matched) if matched else "None", styles["Normal"]))

    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>Missing Skills</b>", styles["Heading2"]))
    missing = score_data.get("missing_skills", [])
    story.append(Paragraph(", ".join(missing) if missing else "None", styles["Normal"]))

    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>Recommendations</b>", styles["Heading2"]))
    for rec in score_data.get("recommendations", []):
        story.append(Paragraph(f"- {rec}", styles["Normal"]))

    doc.build(story)
    logger.info("PDF report generated: %s", output_path.name)
    return output_path
