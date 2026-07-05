import streamlit as st
from frontend.utils.styling import inject_design_css
from frontend.utils.api_client import health_check

st.set_page_config(
    page_title="AI Resume Screening ATS",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_design_css()

if "api_ok" not in st.session_state:
    st.session_state.api_ok = health_check()

st.sidebar.markdown(
    '<div class="headline" style="padding: 16px 0;">AI Resume ATS</div>',
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    '<div class="eyebrow" style="margin-bottom: 24px;">Screening Platform</div>',
    unsafe_allow_html=True,
)

api_status = "🟢 Online" if st.session_state.api_ok else "🔴 Offline"
st.sidebar.markdown(f"<div class='body-sm'>API: {api_status}</div>", unsafe_allow_html=True)

st.sidebar.markdown("---")

nav = st.sidebar.radio(
    "Navigate",
    ["Dashboard", "Upload & Score", "Rankings", "Compare", "Batch Process", "Keyword Analysis", "Reports"],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    '<div class="caption">v1.0 · FastAPI + Streamlit<br>Groq · Gemini · FAISS</div>',
    unsafe_allow_html=True,
)

if nav == "Dashboard":
    from frontend.pages import dashboard
    dashboard.show()
elif nav == "Upload & Score":
    from frontend.pages import upload_score
    upload_score.show()
elif nav == "Rankings":
    from frontend.pages import rankings
    rankings.show()
elif nav == "Compare":
    from frontend.pages import compare
    compare.show()
elif nav == "Batch Process":
    from frontend.pages import batch
    batch.show()
elif nav == "Keyword Analysis":
    from frontend.pages import keyword_analysis
    keyword_analysis.show()
elif nav == "Reports":
    from frontend.pages import reports
    reports.show()
