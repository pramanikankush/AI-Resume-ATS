# ATS Platform Styling & Performance Improvements spec

This spec details the design and implementation of styling fixes, performance caching, and a new feature allowing users to match an uploaded resume with pasted Job Description (JD) text.

## 1. Goal Description
The objective is to:
1. Fix styling issues, particularly the active tab text color (black text on a black background) and the secondary button style.
2. Optimize frontend performance by caching API calls to eliminate lag during Streamlit's script execution.
3. Implement a new option on the scoring page to combine an uploaded resume with pasted JD text.
4. Verify the entire application works seamlessly without errors, checking all sidebar pages.

## 2. Proposed Changes

### 2.1 UI Styling Refinements
We will modify the CSS rules in [styling.py](file:///c:/Users/ankus/Desktop/portfolio%20projects/AI-Resume-Screening-ATS-Platform/frontend/utils/styling.py):
* **Active Tab Contrast**:
  ```css
  .stTabs [aria-selected="true"] * {
      color: var(--inverse-ink) !important;
  }
  ```
  This ensures that any nested label text inside the active tab turns white (`var(--inverse-ink)`) instead of staying black (`var(--ink)`).
* **Button Contrasts**:
  Update button CSS to treat the general `div[data-testid="stButton"] button` as a secondary button (white background, gray border, black text) by default, and explicitly style primary buttons (`kind="primary"` or `data-testid="stBaseButton-primary"`) with a black background and white text.

### 2.2 Performance Optimizations (Caching)
We will edit [api_client.py](file:///c:/Users/ankus/Desktop/portfolio%20projects/AI-Resume-Screening-ATS-Platform/frontend/utils/api_client.py):
* Add `@st.cache_data` to functions:
  * `list_resumes()`
  * `list_jds()`
  * `get_rankings(jd_id)`
  * `get_resume(rid)`
  * `get_jd(jid)`
* Invalidate these caches on mutations:
  * In `upload_file()`: call `list_resumes.clear()`, `list_jds.clear()`, and `get_rankings.clear()`.
  * In `score_resume()` and `score_direct()`: call `get_rankings.clear()` to ensure the FAISS index search list is refreshed.
  * In `clear_all()`: call all clear methods to reset the local cache.

### 2.3 New Feature: Match Uploaded Resume + Pasted JD
We will modify [upload_score.py](file:///c:/Users/ankus/Desktop/portfolio%20projects/AI-Resume-Screening-ATS-Platform/frontend/pages/upload_score.py) to support a hybrid tab:
* Add a third tab: "Upload Resume & Paste JD"
* In this tab:
  * Provide a file uploader for a new resume, AND a dropdown selectbox to choose from already uploaded resumes.
  * Provide a standard text area to paste the Job Description text.
  * When scoring, if a new file is uploaded, upload it to the backend first, then fetch its parsed content or use `/api/score/direct` with the resume's text and the pasted JD text.

## 3. Verification Plan

### Automated/Scripted Verification
We will write a Playwright Python test script to automate loading pages and verify the buttons, tab selections, and file upload flows, ensuring no uncaught exceptions are thrown and caching behaves correctly.

### Manual Verification
Ensure each sidebar item ("Dashboard", "Upload & Score", "Rankings", "Compare", "Batch Process", "Keyword Analysis", "Reports") works without errors and has consistent typography.
