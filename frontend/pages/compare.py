import streamlit as st
import pandas as pd
from frontend.utils.api_client import compare_resumes, list_resumes, list_jds


def show():
    st.markdown('<div class="display-lg">Compare Resumes</div>', unsafe_allow_html=True)

    resumes = list_resumes()
    jds = list_jds()

    if len(resumes) < 2:
        st.info("Upload at least 2 resumes to compare.")
        return

    if not jds:
        st.info("Upload a job description first.")
        return

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        rid_a = st.selectbox(
            "Resume A",
            options=[r["id"] for r in resumes],
            format_func=lambda x: next((r["candidate_name"] for r in resumes if r["id"] == x), x),
        )
    with col_b:
        rid_b = st.selectbox(
            "Resume B",
            options=[r["id"] for r in resumes],
            format_func=lambda x: next((r["candidate_name"] for r in resumes if r["id"] == x), x),
        )
    with col_c:
        jid = st.selectbox(
            "Job Description",
            options=[j["id"] for j in jds],
            format_func=lambda x: next((j["filename"] for j in jds if j["id"] == x), x),
        )

    if st.button("Compare", type="primary"):
        with st.spinner("Comparing..."):
            result = compare_resumes(rid_a, rid_b, jid)

        ra = result["resume_a"]
        rb = result["resume_b"]
        diffs = result["differences"]

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(
                f'<div class="color-block-lilac">'
                f'<div class="card-title">{ra["candidate_name"]}</div>'
                f'<div class="display-xl">{ra["overall_score"]:.0f}</div>'
                f"<div class='body-sm'>ATS Score</div>"
                f"</div>",
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                f'<div class="color-block-coral">'
                f'<div class="card-title">{rb["candidate_name"]}</div>'
                f'<div class="display-xl">{rb["overall_score"]:.0f}</div>'
                f"<div class='body-sm'>ATS Score</div>"
                f"</div>",
                unsafe_allow_html=True,
            )
        with col3:
            diff = diffs["overall_diff"]
            st.markdown(
                f'<div class="color-block-cream">'
                f'<div class="card-title">Difference</div>'
                f'<div class="display-xl">{"+" if diff > 0 else ""}{diff:.1f}</div>'
                f"<div class='body-sm'>Points</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'>Score Breakdown</div>", unsafe_allow_html=True)

        breakdown = []
        for key in ["keyword_match", "semantic_match", "skills_coverage", "experience_relevance", "education_match"]:
            breakdown.append({
                "Metric": key.replace("_", " ").title(),
                ra["candidate_name"]: ra.get(key, 0),
                rb["candidate_name"]: rb.get(key, 0),
            })
        df = pd.DataFrame(breakdown)
        st.dataframe(df, use_container_width=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'>Skills Difference</div>", unsafe_allow_html=True)
        col_x, col_y = st.columns(2)
        with col_x:
            st.markdown(f"<div class='body-sm'><b>Unique to {ra['candidate_name']}:</b></div>", unsafe_allow_html=True)
            if diffs["skills_diff"]:
                for s in diffs["skills_diff"]:
                    st.markdown(f"<span class='score-badge score-high' style='margin:4px;'>{s}</span>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='body-sm'>None</div>", unsafe_allow_html=True)
        with col_y:
            st.markdown(f"<div class='body-sm'><b>Unique to {rb['candidate_name']}:</b></div>", unsafe_allow_html=True)
            if diffs["missing_diff"]:
                for s in diffs["missing_diff"]:
                    st.markdown(f"<span class='score-badge score-low' style='margin:4px;'>{s}</span>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='body-sm'>None</div>", unsafe_allow_html=True)
