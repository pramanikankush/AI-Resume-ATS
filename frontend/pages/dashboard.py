import streamlit as st
import pandas as pd
from frontend.utils.api_client import list_resumes, list_jds, get_rankings


def show():
    st.markdown('<div class="display-lg">Dashboard</div>', unsafe_allow_html=True)

    resumes = list_resumes()
    jds = list_jds()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            f"""<div class="metric-card">
                <div class="metric-value">{len(resumes)}</div>
                <div class="metric-label">Resumes</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""<div class="metric-card">
                <div class="metric-value">{len(jds)}</div>
                <div class="metric-label">Job Descriptions</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with col3:
        ranked = 0
        if jds:
            try:
                r = get_rankings(jds[0]["id"])
                ranked = r.get("total_candidates", 0)
            except Exception:
                pass
        st.markdown(
            f"""<div class="metric-card">
                <div class="metric-value">{ranked}</div>
                <div class="metric-label">Ranked Candidates</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            f"""<div class="metric-card">
                <div class="metric-value">{'🟢' if st.session_state.get('api_ok') else '🔴'}</div>
                <div class="metric-label">API Status</div>
            </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Quick Actions</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(
            '<div class="color-block-lime">'
            '<div class="card-title">Upload Resumes</div>'
            '<div class="body">Upload PDF, DOCX, or TXT files to get started.</div>'
            "</div>",
            unsafe_allow_html=True,
        )
    with col_b:
        st.markdown(
            '<div class="color-block-lilac">'
            '<div class="card-title">Score & Rank</div>'
            '<div class="body">Match resumes against job descriptions instantly.</div>'
            "</div>",
            unsafe_allow_html=True,
        )

    if resumes:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">Recent Resumes</div>', unsafe_allow_html=True)
        df = pd.DataFrame(resumes)
        st.dataframe(df, use_container_width=True)
