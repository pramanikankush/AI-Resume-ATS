# Styling, Caching, and Hybrid Match Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Polish the ATS styling issues, introduce robust Streamlit caching to speed up navigation, and add a third page tab to score an uploaded resume against a typed/pasted JD.

**Architecture:** Update styling CSS tokens, decorate HTTP client functions with Streamlit's `@st.cache_data` caching (with target invalidation on mutations), and introduce a third layout tab utilizing raw text extraction for direct scoring.

**Tech Stack:** Streamlit (Python), FastAPI, CSS.

---

### Task 1: UI Styling Polish

**Files:**
* Modify: [styling.py](file:///c:/Users/ankus/Desktop/portfolio%20projects/AI-Resume-Screening-ATS-Platform/frontend/utils/styling.py)

- [ ] **Step 1: Update Active Tab styling**
  Find the `.stTabs [aria-selected="true"]` rule and add a child selector rule so child text nodes render as white:
  ```css
  .stTabs [aria-selected="true"] * {
      color: var(--inverse-ink) !important;
  }
  ```

- [ ] **Step 2: Restructure Button styles**
  Replace the button styles so the base `button` rule styles secondary buttons, and specific attributes override it for primary:
  ```css
  /* Pill buttons - general / secondary style by default */
  div[data-testid="stButton"] button {
      border-radius: 50px !important;
      font-size: 20px !important;
      font-weight: 480 !important;
      padding: 10px 24px !important;
      background: var(--canvas) !important;
      color: var(--ink) !important;
      border: 1px solid var(--hairline) !important;
      font-family: 'Inter', sans-serif !important;
      transition: transform 0.1s ease !important;
      line-height: 1.4 !important;
      letter-spacing: -0.10px !important;
      height: auto !important;
  }
  /* Primary buttons override */
  div[data-testid="stButton"] button[kind="primary"],
  div[data-testid="stButton"] button[data-testid="stBaseButton-primary"] {
      background: var(--ink) !important;
      color: var(--on-primary) !important;
      border: none !important;
  }
  /* Hover and active states */
  div[data-testid="stButton"] button:hover {
      opacity: 0.85 !important;
  }
  div[data-testid="stButton"] button:active,
  div[data-testid="stButton"] button:focus:active {
      transform: scale(0.96) !important;
  }
  ```

- [ ] **Step 3: Verify visually**
  Refresh the Streamlit page at `http://localhost:8501`. Ensure the selected tab is legible and secondary/primary buttons look correct.

- [ ] **Step 4: Commit styling changes**
  ```bash
  git add frontend/utils/styling.py
  git commit -m "style: fix active tab visibility and secondary button contrast"
  ```

---

### Task 2: Streamlit Caching

**Files:**
* Modify: [api_client.py](file:///c:/Users/ankus/Desktop/portfolio%20projects/AI-Resume-Screening-ATS-Platform/frontend/utils/api_client.py)

- [ ] **Step 1: Add cache decorators to list/get calls**
  Decorate `list_resumes`, `list_jds`, `get_rankings`, `get_resume`, `get_jd`, and `get_keyword_analysis` with `@st.cache_data`.
  ```python
  @st.cache_data
  def list_resumes() -> list[dict]:
      ...

  @st.cache_data
  def list_jds() -> list[dict]:
      ...

  @st.cache_data
  def get_rankings(jd_id: str) -> dict:
      ...

  @st.cache_data
  def get_resume(rid: str) -> dict:
      ...

  @st.cache_data
  def get_jd(jid: str) -> dict:
      ...

  @st.cache_data
  def get_keyword_analysis(resume_id: str, jd_id: str = "") -> list:
      ...
  ```

- [ ] **Step 2: Clear caches on mutations**
  Add cache invalidation inside mutation calls:
  * In `upload_file`:
    ```python
    list_resumes.clear()
    list_jds.clear()
    get_rankings.clear()
    ```
  * In `score_resume` and `score_direct`:
    ```python
    get_rankings.clear()
    ```
  * In `clear_all`:
    ```python
    list_resumes.clear()
    list_jds.clear()
    get_rankings.clear()
    get_resume.clear()
    get_jd.clear()
    get_keyword_analysis.clear()
    ```

- [ ] **Step 3: Verify cache invalidation**
  Click tabs on the Streamlit dashboard. Ensure transitions are instant. Upload a mock file, check that the list is refreshed immediately.

- [ ] **Step 4: Commit caching changes**
  ```bash
  git add frontend/utils/api_client.py
  git commit -m "perf: add Streamlit caching for API lookups with cache clearing on mutation"
  ```

---

### Task 3: Hybrid Score Tab

**Files:**
* Modify: [upload_score.py](file:///c:/Users/ankus/Desktop/portfolio%20projects/AI-Resume-Screening-ATS-Platform/frontend/pages/upload_score.py)

- [ ] **Step 1: Update tabs selection**
  Change the tabs declaration to include a third hybrid option:
  ```python
  tab1, tab2, tab3 = st.tabs(["Upload Files", "Paste Text", "Upload Resume & Paste JD"])
  ```

- [ ] **Step 2: Implement hybrid tab rendering**
  Implement the view in `with tab3:` where the user can choose an uploaded resume or upload a new one, paste the JD text in a text area, and click score.
  ```python
  with tab3:
      st.markdown('<div class="section-header">Hybrid: Uploaded Resume + Pasted JD</div>', unsafe_allow_html=True)
      
      # Select or Upload Resume
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
          r_file = st.file_uploader("Upload new resume", type=["pdf", "docx", "txt"], key="hybrid_resume_upload")
          if r_file and st.button("Upload Resume", key="hybrid_up_resume"):
              with st.spinner("Uploading..."):
                  resp = upload_resume(r_file)
                  st.session_state["last_resume"] = resp["id"]
                  st.success(f"Uploaded: {resp['candidate_name']}")
                  st.rerun()

      # If a new resume was just uploaded, set it as active
      if st.session_state.get("last_resume") and (not rid or st.session_state["last_resume"] != rid):
          rid = st.session_state["last_resume"]

      # JD Paste Box
      jd_text = st.text_area("Job Description Text", height=200, placeholder="Paste job description here...", key="hybrid_jd_text")
      
      if st.button("Score Hybrid", type="primary", key="hybrid_score_btn"):
          if not rid:
              st.error("Please upload or select a resume.")
          elif not jd_text.strip():
              st.error("Please paste the Job Description.")
          else:
              with st.spinner("Analyzing..."):
                  from frontend.utils.api_client import get_resume, score_direct
                  # Fetch resume text
                  res_details = get_resume(rid)
                  res_text = res_details.get("raw_text", "")
                  candidate = res_details.get("candidate_name", "Candidate")
                  
                  # Score direct
                  score = score_direct(res_text, jd_text, candidate)
                  st.session_state["last_score"] = score
                  st.session_state["last_resume"] = rid
              _render_score(score)
  ```

- [ ] **Step 3: Verify the tab manually**
  Navigate to the "Upload & Score" page, go to the "Upload Resume & Paste JD" tab, select a resume, paste a JD description, click "Score Hybrid", and verify the score output is rendered cleanly.

- [ ] **Step 4: Commit hybrid tab changes**
  ```bash
  git add frontend/pages/upload_score.py
  git commit -m "feat: add hybrid 'Upload Resume & Paste JD' tab to upload_score page"
  ```

---

### Task 4: E2E Verification Script

**Files:**
* Create: [verify_ats.py](file:///c:/Users/ankus/Desktop/portfolio%20projects/AI-Resume-Screening-ATS-Platform/scratch/verify_ats.py)

- [ ] **Step 1: Write verification script**
  Create a Playwright automation script `scratch/verify_ats.py` that visits each sidebar option and asserts no exceptions are raised.
  ```python
  import time
  from playwright.sync_api import sync_playwright

  def run_test():
      with sync_playwright() as p:
          browser = p.chromium.launch(headless=True)
          page = browser.new_page()
          page.goto('http://localhost:8501')
          page.wait_for_load_state('networkidle')
          print("Page loaded successfully.")
          
          # Nav items to check
          nav_items = ["Dashboard", "Upload & Score", "Rankings", "Compare", "Batch Process", "Keyword Analysis", "Reports"]
          for nav in nav_items:
              print(f"Testing sidebar page: {nav}")
              # Click radio button option matching the label
              page.click(f"text={nav}")
              page.wait_for_timeout(1000)
              
              # Assert no Streamlit uncaught app exception is visible in page content
              content = page.content()
              if "Uncaught app exception" in content or "Traceback" in content:
                  raise Exception(f"Uncaught exception found on page: {nav}")
                  
          print("All pages tested successfully without uncaught exceptions!")
          browser.close()

  if __name__ == "__main__":
      run_test()
  ```

- [ ] **Step 2: Run verification script**
  Run: `python scratch/verify_ats.py`
  Expected: Prints "All pages tested successfully without uncaught exceptions!"

- [ ] **Step 3: Commit verification script**
  ```bash
  git add scratch/verify_ats.py
  git commit -m "test: add automated end-to-end verification script for Streamlit pages"
  ```
