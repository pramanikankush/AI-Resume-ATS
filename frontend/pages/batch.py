import streamlit as st
import pandas as pd
from frontend.utils.api_client import start_batch, list_jds, list_resumes


def show():
    st.markdown('<div class="display-lg">Batch Processing</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="color-block-lime">'
        '<div class="body-lg">Score all uploaded resumes against a job description in one run.</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    resumes = []
    jds = []
    try:
        resumes = list_resumes()
    except Exception:
        pass
    try:
        jds = list_jds()
    except Exception:
        pass

    if not resumes:
        st.markdown(
            '<div class="color-block-cream" style="padding:24px 48px;">'
            '<div class="body">No resumes uploaded yet. Go to Upload & Score to add resumes first.</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        return
    if not jds:
        st.markdown(
            '<div class="color-block-cream" style="padding:24px 48px;">'
            '<div class="body">No job descriptions uploaded yet. Go to Upload & Score to add one first.</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        return

    st.markdown(f'<div class="body-sm">{len(resumes)} resumes available for batch scoring</div>', unsafe_allow_html=True)

    jid = st.selectbox(
        "Job Description",
        options=[j["id"] for j in jds],
        format_func=lambda x: next((j["filename"] for j in jds if j["id"] == x), x),
    )

    if st.button("Run Batch", type="primary"):
        with st.spinner("Scoring all resumes..."):
            try:
                result = start_batch(jid)
            except Exception as e:
                st.error(f"Batch processing failed: {e}")
                return

        st.session_state["batch_result"] = result

    if "batch_result" in st.session_state:
        s = st.session_state["batch_result"]

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(
                f'<div class="metric-card"><div class="metric-value">{s.get("total", 0)}</div>'
                f'<div class="metric-label">Total</div></div>',
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                f'<div class="metric-card"><div class="metric-value">{s.get("completed", 0)}</div>'
                f'<div class="metric-label">Completed</div></div>',
                unsafe_allow_html=True,
            )
        with col3:
            st.markdown(
                f'<div class="metric-card"><div class="metric-value">{s.get("failed", 0)}</div>'
                f'<div class="metric-label">Failed</div></div>',
                unsafe_allow_html=True,
            )

        results = s.get("results", [])
        if results:
            rows = []
            for r in results:
                if isinstance(r, dict):
                    rows.append(r)
                else:
                    rows.append(r.dict() if hasattr(r, 'dict') else r.model_dump())
            df = pd.DataFrame(rows)
            display_cols = [c for c in ["candidate_name", "overall_score", "keyword_match", "semantic_match", "skills_coverage"] if c in df.columns]
            if display_cols:
                df_display = df[display_cols].copy()
                df_display.columns = [c.replace("_", " ").title() for c in display_cols]
                st.dataframe(df_display, use_container_width=True)

                st.markdown('<hr>', unsafe_allow_html=True)
                st.markdown('<div class="section-header">Score Distribution</div>', unsafe_allow_html=True)
                chart_col = "Overall Score" if "Overall Score" in df_display.columns else df_display.columns[1]
                st.bar_chart(df_display.set_index(df_display.columns[0])[chart_col], height=300)

                csv = df_display.to_csv(index=False)
                st.download_button("Export CSV", csv, file_name="batch_results.csv", mime="text/csv")
        else:
            st.markdown(
                '<div class="color-block-cream" style="padding:24px 48px;">'
                '<div class="body">No results were generated. Make sure resumes have been uploaded.</div>'
                '</div>',
                unsafe_allow_html=True,
            )
