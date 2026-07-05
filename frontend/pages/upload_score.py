import streamlit as st
from frontend.utils.api_client import upload_resume, upload_jd, score_resume, list_resumes, list_jds, score_direct, get_resume


def _score_badge(val: float) -> str:
    if val >= 75:
        return f'<span class="score-badge score-high">{val:.0f}</span>'
    elif val >= 50:
        return f'<span class="score-badge score-mid">{val:.0f}</span>'
    return f'<span class="score-badge score-low">{val:.0f}</span>'


def show():
    st.markdown('<div class="display-lg">Upload & Score</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Upload Files", "Paste Text", "Upload Resume & Paste JD"])

    with tab1:
        col_l, col_r = st.columns(2)
        with col_l:
            st.markdown('<div class="section-header">Resume</div>', unsafe_allow_html=True)
            r_file = st.file_uploader("Upload resume", type=["pdf", "docx", "txt"], key="resume_upload")
            if r_file and st.button("Upload Resume", key="up_resume"):
                with st.spinner("Uploading..."):
                    resp = upload_resume(r_file)
                    st.session_state["last_resume"] = resp["id"]
                    st.success(f"Uploaded: {resp['candidate_name']}")

        with col_r:
            st.markdown('<div class="section-header">Job Description</div>', unsafe_allow_html=True)
            j_file = st.file_uploader("Upload JD", type=["pdf", "docx", "txt"], key="jd_upload")
            if j_file and st.button("Upload JD", key="up_jd"):
                with st.spinner("Uploading..."):
                    resp = upload_jd(j_file)
                    st.session_state["last_jd"] = resp["id"]
                    st.success(f"Uploaded: {resp['title']}")

        st.markdown("<hr>", unsafe_allow_html=True)

        resumes = list_resumes()
        jds = list_jds()

        if resumes and jds:
            col_a, col_b, _ = st.columns([2, 2, 1])
            with col_a:
                rid = st.selectbox(
                    "Select Resume",
                    options=[r["id"] for r in resumes],
                    format_func=lambda x: next((r["candidate_name"] for r in resumes if r["id"] == x), x),
                )
            with col_b:
                jid = st.selectbox(
                    "Select Job Description",
                    options=[j["id"] for j in jds],
                    format_func=lambda x: next((j["filename"] for j in jds if j["id"] == x), x),
                )

            if st.button("Score", type="primary"):
                with st.spinner("Analyzing..."):
                    score = score_resume(rid, jid)
                    st.session_state["last_score"] = score
                _render_score(score)

        if st.session_state.get("last_score") and not (resumes and jds):
            _render_score(st.session_state["last_score"])

    with tab2:
        st.markdown('<div class="section-header">Paste & Score</div>', unsafe_allow_html=True)
        resume_text = st.text_area("Resume Text", height=200, placeholder="Paste resume content here...", key="paste_resume_text")
        jd_text = st.text_area("Job Description Text", height=200, placeholder="Paste job description here...", key="paste_jd_text")
        candidate = st.text_input("Candidate Name", value="Candidate", key="paste_candidate_name")

        if st.button("Score Direct", type="primary", key="paste_score_btn") and resume_text and jd_text:
            with st.spinner("Analyzing..."):
                score = score_direct(resume_text, jd_text, candidate)
                st.session_state["last_score"] = score
            _render_score(score)

    with tab3:
        st.markdown('<div class="section-header">Hybrid: Uploaded Resume + Pasted JD</div>', unsafe_allow_html=True)
        
        resumes = list_resumes()
        rid = None
        
        col_resume_select, col_resume_upload = st.columns(2)
        with col_resume_select:
            st.markdown('<div class="body-sm"><b>Select Uploaded Resume</b></div>', unsafe_allow_html=True)
            if resumes:
                rid = st.selectbox(
                    "Choose Resume",
                    options=[r["id"] for r in resumes],
                    format_func=lambda x: next((r["candidate_name"] for r in resumes if r["id"] == x), x),
                    key="hybrid_resume_select"
                )
            else:
                st.info("No resumes uploaded yet. Upload one on the right.")
                
        with col_resume_upload:
            st.markdown('<div class="body-sm"><b>Or Upload New Resume</b></div>', unsafe_allow_html=True)
            r_file_hybrid = st.file_uploader("Upload new resume", type=["pdf", "docx", "txt"], key="hybrid_resume_upload")
            if r_file_hybrid and st.button("Upload Resume", key="hybrid_up_resume"):
                with st.spinner("Uploading..."):
                    resp = upload_resume(r_file_hybrid)
                    st.session_state["last_resume"] = resp["id"]
                    st.success(f"Uploaded: {resp['candidate_name']}")
                    st.rerun()

        if st.session_state.get("last_resume") and (not rid or st.session_state["last_resume"] != rid):
            rid = st.session_state["last_resume"]

        jd_text_hybrid = st.text_area("Job Description Text", height=200, placeholder="Paste job description here...", key="hybrid_jd_text")
        
        if st.button("Score Hybrid", type="primary", key="hybrid_score_btn"):
            if not rid:
                st.error("Please upload or select a resume.")
            elif not jd_text_hybrid.strip():
                st.error("Please paste the Job Description.")
            else:
                with st.spinner("Analyzing..."):
                    res_details = get_resume(rid)
                    res_text = res_details.get("raw_text", "")
                    candidate = res_details.get("candidate_name", "Candidate")
                    
                    score = score_direct(res_text, jd_text_hybrid, candidate)
                    st.session_state["last_score"] = score
                    st.session_state["last_resume"] = rid
                _render_score(score)


    if st.session_state.get("last_score"):
        score = st.session_state["last_score"]
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">Report</div>', unsafe_allow_html=True)
        if st.button("Generate PDF Report"):
            try:
                from frontend.utils.api_client import download_report
                pdf = download_report(
                    st.session_state.get("last_resume", score.get("resume_id", "")),
                    st.session_state.get("last_jd", ""),
                )
                st.download_button("Download PDF", pdf, file_name="ats_report.pdf", mime="application/pdf")
            except Exception as e:
                st.error(f"PDF generation requires file-based upload: {e}")


def _render_score(score: dict):
    s = score
    st.markdown('<div class="color-block-cream">', unsafe_allow_html=True)
    c_col1, c_col2 = st.columns([1, 2])
    with c_col1:
        overall = s.get("overall_score", 0)
        st.markdown(
            f'<div style="text-align:center;">'
            f'<div class="display-xl">{overall:.0f}</div>'
            f'<div class="body-sm">Overall ATS Score</div>'
            f"</div>",
            unsafe_allow_html=True,
        )
    with c_col2:
        st.markdown(f"<div class='card-title'>{s.get('candidate_name', 'Candidate')}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='body-sm'>Resume ID: {s.get('resume_id', '')}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    col_a, col_b, col_c, col_d, col_e = st.columns(5)
    labels = [
        ("keyword_match", "Keywords"),
        ("semantic_match", "Semantic"),
        ("skills_coverage", "Skills"),
        ("experience_relevance", "Experience"),
        ("education_match", "Education"),
    ]
    for col, (key, label) in zip([col_a, col_b, col_c, col_d, col_e], labels):
        with col:
            val = s.get(key, 0)
            st.markdown(
                f'<div class="metric-card">'
                f'<div class="metric-value" style="font-size: 32px;">{val:.0f}</div>'
                f'<div class="metric-label">{label}</div>'
                f"</div>",
                unsafe_allow_html=True,
            )

    st.markdown("<hr>", unsafe_allow_html=True)
    col_sk, col_miss = st.columns(2)
    with col_sk:
        st.markdown("<div class='section-header'>Matched Skills</div>", unsafe_allow_html=True)
        matched = s.get("matched_skills", [])
        if matched:
            for skill in matched:
                st.markdown(
                    f'<span class="score-badge score-high" style="margin: 4px;">{skill}</span>',
                    unsafe_allow_html=True,
                )
        else:
            st.markdown("<div class='body'>No skills matched</div>", unsafe_allow_html=True)

    with col_miss:
        st.markdown("<div class='section-header'>Missing Skills</div>", unsafe_allow_html=True)
        missing = s.get("missing_skills", [])
        if missing:
            for skill in missing:
                st.markdown(
                    f'<span class="score-badge score-low" style="margin: 4px;">{skill}</span>',
                    unsafe_allow_html=True,
                )
        else:
            st.markdown("<div class='body'>All skills present</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>Recommendations</div>", unsafe_allow_html=True)
    for rec in s.get("recommendations", []):
        st.markdown(f"<div class='body'>→ {rec}</div>", unsafe_allow_html=True)
