import streamlit as st
from frontend.utils.api_client import list_resumes, list_jds, download_report


def show():
    st.markdown('<div class="display-lg">PDF Reports</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="color-block-lilac">'
        '<div class="body-lg">Generate detailed ATS analysis reports as downloadable PDFs.</div>'
        "</div>",
        unsafe_allow_html=True,
    )

    resumes = list_resumes()
    jds = list_jds()

    if not resumes or not jds:
        st.info("Upload both a resume and a job description to generate a report.")
        return

    col1, col2 = st.columns(2)
    with col1:
        rid = st.selectbox(
            "Resume",
            options=[r["id"] for r in resumes],
            format_func=lambda x: next((r["candidate_name"] for r in resumes if r["id"] == x), x),
        )
    with col2:
        jid = st.selectbox(
            "Job Description",
            options=[j["id"] for j in jds],
            format_func=lambda x: next((j["filename"] for j in jds if j["id"] == x), x),
        )

    if st.button("Generate PDF Report", type="primary"):
        with st.spinner("Generating report..."):
            try:
                pdf_bytes = download_report(rid, jid)
                st.success("Report generated!")
                st.download_button(
                    "Download PDF",
                    pdf_bytes,
                    file_name="ats_report.pdf",
                    mime="application/pdf",
                )
            except Exception as e:
                st.error(f"Report generation failed: {e}")
