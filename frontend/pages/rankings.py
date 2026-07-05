import streamlit as st
import pandas as pd
from frontend.utils.api_client import get_rankings, list_jds


def show():
    st.markdown('<div class="display-lg">Candidate Rankings</div>', unsafe_allow_html=True)

    jds = list_jds()
    if not jds:
        st.info("Upload a job description first to generate rankings.")
        return

    jid = st.selectbox(
        "Select Job Description",
        options=[j["id"] for j in jds],
        format_func=lambda x: next((j["filename"] for j in jds if j["id"] == x), x),
    )

    if st.button("Rank Candidates", type="primary"):
        with st.spinner("Ranking..."):
            data = get_rankings(jid)
        rankings = data.get("rankings", [])
        total = data.get("total_candidates", 0)

        st.markdown(
            f'<div class="color-block-mint">'
            f'<div class="headline">{total} Candidates Ranked</div>'
            f"</div>",
            unsafe_allow_html=True,
        )

        if rankings:
            df = pd.DataFrame(rankings)
            df["score"] = df["score"].apply(lambda x: round(x * 100, 1))
            df = df.rename(columns={"score": "Match Score", "candidate_name": "Candidate", "resume_id": "ID"})
            df["Rank"] = range(1, len(df) + 1)
            df = df[["Rank", "Candidate", "Match Score"]]
            st.dataframe(df, use_container_width=True)

            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("<div class='section-header'>Score Distribution</div>", unsafe_allow_html=True)

            chart_data = pd.DataFrame({"score": df["Match Score"]})
            st.bar_chart(chart_data, height=300)

            if st.button("Export CSV"):
                csv = df.to_csv(index=False)
                st.download_button("Download CSV", csv, file_name="rankings.csv", mime="text/csv")
        else:
            st.info("No candidates ranked yet. Upload and score resumes first.")
