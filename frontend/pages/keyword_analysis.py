import streamlit as st
import pandas as pd
from frontend.utils.api_client import get_keyword_analysis, list_resumes, list_jds


def show():
    st.markdown('<div class="display-lg">Keyword Analysis</div>', unsafe_allow_html=True)

    resumes = list_resumes()
    jds = list_jds()

    if not resumes:
        st.info("Upload a resume first.")
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
            "Job Description (optional)",
            options=[""] + [j["id"] for j in jds],
            format_func=lambda x: "None" if not x else next(
                (j["filename"] for j in jds if j["id"] == x), x
            ),
        )

    if st.button("Analyze", type="primary"):
        with st.spinner("Analyzing keywords..."):
            keywords = get_keyword_analysis(rid, jid)

        st.markdown(f"<div class='body-sm'>{len(keywords)} keywords found</div>", unsafe_allow_html=True)

        if keywords:
            df = pd.DataFrame(keywords)
            st.dataframe(df, use_container_width=True)

            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("<div class='section-header'>Top Keywords</div>", unsafe_allow_html=True)

            top = df.head(15)
            chart = pd.DataFrame({"keyword": top["keyword"], "frequency": top["frequency"]}).set_index("keyword")
            st.bar_chart(chart, height=350)

            present = sum(1 for k in keywords if k["is_present"])
            st.markdown(
                f"<div class='color-block-mint'>"
                f"<div class='body-lg'>{present}/{len(keywords)} keywords match the job description</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

            csv = df.to_csv(index=False)
            st.download_button("Export CSV", csv, file_name="keyword_analysis.csv", mime="text/csv")
