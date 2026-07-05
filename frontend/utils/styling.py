DESIGN_CSS = """
<!-- Google Fonts Import for Inter (Variable Weights) and JetBrains Mono (Variable Weights) -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&family=JetBrains+Mono:wght@100..800&display=swap" rel="stylesheet">

<style>
    /* === DESIGN.md Tokens === */
    :root {
        --primary: #000000;
        --on-primary: #ffffff;
        --ink: #000000;
        --canvas: #ffffff;
        --inverse-canvas: #000000;
        --inverse-ink: #ffffff;
        --surface-soft: #f7f7f5;
        --hairline: #e6e6e6;
        --hairline-soft: #f1f1f1;
        --block-lime: #dceeb1;
        --block-lilac: #c5b0f4;
        --block-cream: #f4ecd6;
        --block-mint: #c8e6cd;
        --block-pink: #efd4d4;
        --block-coral: #f3c9b6;
        --block-navy: #1f1d3d;
        --accent-magenta: #ff3d8b;
        --semantic-success: #1ea64a;
    }

    /* Core fonts reset */
    .stApp {
        background: var(--canvas) !important;
        color: var(--ink) !important;
    }
    .stApp, .stApp * {
        font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    }

    /* Typography tokens */
    .display-xl {
        font-family: 'Inter', sans-serif !important;
        font-size: 86px !important;
        font-weight: 340 !important;
        line-height: 1.0 !important;
        letter-spacing: -1.72px !important;
    }
    .display-lg {
        font-family: 'Inter', sans-serif !important;
        font-size: 64px !important;
        font-weight: 340 !important;
        line-height: 1.1 !important;
        letter-spacing: -0.96px !important;
        margin-bottom: 24px;
    }
    .headline {
        font-family: 'Inter', sans-serif !important;
        font-size: 26px !important;
        font-weight: 540 !important;
        line-height: 1.35 !important;
        letter-spacing: -0.26px !important;
    }
    .subhead {
        font-family: 'Inter', sans-serif !important;
        font-size: 26px !important;
        font-weight: 340 !important;
        line-height: 1.35 !important;
        letter-spacing: -0.26px !important;
    }
    .card-title {
        font-family: 'Inter', sans-serif !important;
        font-size: 24px !important;
        font-weight: 700 !important;
        line-height: 1.45 !important;
        margin-bottom: 12px;
    }
    .body-lg {
        font-family: 'Inter', sans-serif !important;
        font-size: 20px !important;
        font-weight: 330 !important;
        line-height: 1.4 !important;
        letter-spacing: -0.14px !important;
    }
    .body {
        font-family: 'Inter', sans-serif !important;
        font-size: 18px !important;
        font-weight: 320 !important;
        line-height: 1.45 !important;
        letter-spacing: -0.26px !important;
    }
    .body-sm {
        font-family: 'Inter', sans-serif !important;
        font-size: 16px !important;
        font-weight: 330 !important;
        line-height: 1.45 !important;
        letter-spacing: -0.14px !important;
    }
    .button-text {
        font-family: 'Inter', sans-serif !important;
        font-size: 20px !important;
        font-weight: 480 !important;
        line-height: 1.4 !important;
        letter-spacing: -0.10px !important;
    }
    .eyebrow {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 18px !important;
        font-weight: 400 !important;
        line-height: 1.3 !important;
        letter-spacing: 0.54px !important;
        text-transform: uppercase !important;
    }
    .caption {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 12px !important;
        font-weight: 400 !important;
        line-height: 1.0 !important;
        letter-spacing: 0.60px !important;
        text-transform: uppercase !important;
    }

    .main-header {
        font-family: 'Inter', sans-serif !important;
        font-size: 64px;
        font-weight: 340;
        line-height: 1.1;
        letter-spacing: -0.96px;
        color: var(--ink);
        margin-bottom: 0.25em;
    }

    .section-header {
        font-family: 'Inter', sans-serif !important;
        font-size: 26px;
        font-weight: 540;
        line-height: 1.35;
        letter-spacing: -0.26px;
        color: var(--ink);
        margin-top: 24px;
        margin-bottom: 16px;
    }

    /* Color-block sections with 48px padding (spacing.xxl) and 24px corners (rounded.lg) */
    .color-block-lime, .color-block-lilac, .color-block-navy, .color-block-mint, .color-block-coral, .color-block-cream {
        border-radius: 24px !important;
        padding: 48px !important;
        margin: 32px 0 !important;
        border: 1px solid var(--hairline);
    }
    .color-block-lime { background: var(--block-lime) !important; color: var(--ink) !important; }
    .color-block-lilac { background: var(--block-lilac) !important; color: var(--ink) !important; }
    .color-block-navy { background: var(--block-navy) !important; color: var(--inverse-ink) !important; border: none !important; }
    .color-block-mint { background: var(--block-mint) !important; color: var(--ink) !important; }
    .color-block-coral { background: var(--block-coral) !important; color: var(--ink) !important; }
    .color-block-cream { background: var(--block-cream) !important; color: var(--ink) !important; }

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
    div[data-testid="stButton"] button * {
        color: var(--ink) !important;
    }
    /* Primary buttons override */
    div[data-testid="stButton"] button[kind="primary"],
    div[data-testid="stButton"] button[data-testid="stBaseButton-primary"] {
        background: var(--ink) !important;
        color: var(--on-primary) !important;
        border: none !important;
    }
    div[data-testid="stButton"] button[kind="primary"] *,
    div[data-testid="stButton"] button[data-testid="stBaseButton-primary"] * {
        color: var(--on-primary) !important;
    }
    /* Hover and active states */
    div[data-testid="stButton"] button:hover {
        opacity: 0.85 !important;
    }
    div[data-testid="stButton"] button:active,
    div[data-testid="stButton"] button:focus:active {
        transform: scale(0.96) !important;
    }



    /* Metric cards with rounded.lg (24px) */
    .metric-card {
        background: var(--surface-soft);
        border-radius: 24px;
        padding: 24px;
        text-align: center;
        border: 1px solid var(--hairline-soft);
    }
    .metric-value {
        font-family: 'Inter', sans-serif !important;
        font-size: 48px;
        font-weight: 340;
        line-height: 1;
    }
    .metric-label {
        font-family: 'Inter', sans-serif !important;
        font-size: 16px;
        font-weight: 330;
        color: var(--ink);
        margin-top: 8px;
    }

    /* Form inputs and text areas with rounded.md (8px) and custom focus */
    .stTextInput > div > div, .stTextArea > div > div, .stSelectbox > div > div {
        border-radius: 8px !important;
        border: 1px solid var(--hairline) !important;
        background-color: var(--canvas) !important;
    }
    .stTextInput input, .stTextArea textarea {
        font-family: 'Inter', sans-serif !important;
        color: var(--ink) !important;
    }

    /* Data frame / table customization */
    .dataframe {
        border-radius: 8px !important;
        border: 1px solid var(--hairline-soft) !important;
    }

    /* Score badges (pills) */
    .score-badge {
        display: inline-block;
        background: var(--ink);
        color: var(--inverse-ink);
        border-radius: 50px;
        padding: 6px 18px;
        font-size: 16px;
        font-weight: 480;
        letter-spacing: -0.10px;
    }
    .score-high { background: var(--semantic-success) !important; color: var(--inverse-ink) !important; }
    .score-mid { background: var(--block-lilac) !important; color: var(--ink) !important; }
    .score-low { background: var(--block-coral) !important; color: var(--ink) !important; }

    /* Hide default sidebar navigation */
    div[data-testid="stSidebarNav"] {
        display: none !important;
    }

    /* Sidebar with surface-soft and hairline-soft divider */
    section[data-testid="stSidebar"] {
        background: var(--surface-soft) !important;
        border-right: 1px solid var(--hairline-soft) !important;
    }

    /* Force all text in sidebar to be visible ink */
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] * {
        color: var(--ink) !important;
    }

    /* Customize Streamlit sidebar radio button options */
    div[data-testid="stRadio"] label {
        color: var(--ink) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 18px !important;
        font-weight: 330 !important;
        line-height: 1.45 !important;
        letter-spacing: -0.26px !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] {
        gap: 8px !important;
    }
    /* Style radio dots to match Figma's monochrome style */
    div[data-testid="stRadio"] div[role="radiogroup"] label div:first-child {
        border-color: var(--ink) !important;
        background-color: var(--canvas) !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label input:checked + div {
        background-color: var(--ink) !important;
        border-color: var(--ink) !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label input:checked + div > div {
        background-color: var(--canvas) !important;
    }

    /* Streamlit tabs matching pricing-tab specifications */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        border-bottom: none !important;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 50px !important;
        font-size: 18px !important;
        font-weight: 480 !important;
        padding: 8px 24px !important;
        border: 1px solid var(--hairline) !important;
        background: var(--canvas) !important;
        color: var(--ink) !important;
    }
    .stTabs [aria-selected="true"] {
        background: var(--ink) !important;
        color: var(--inverse-ink) !important;
        border-color: var(--ink) !important;
    }
    .stTabs [aria-selected="true"] * {
        color: var(--inverse-ink) !important;
    }


    /* Expander header styling */
    .streamlit-expanderHeader {
        background: var(--surface-soft) !important;
        border-radius: 8px !important;
        font-weight: 480 !important;
        border: 1px solid var(--hairline-soft) !important;
    }

    hr {
        border: 0 !important;
        border-top: 1px solid var(--hairline-soft) !important;
        margin: 32px 0 !important;
        height: 1px !important;
    }

    .stAlert {
        border-radius: 8px !important;
    }

    /* Clean Chrome removal */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* === Text visibility fixes for Streamlit alerts === */
    /* Info box: use block-cream background with ink text */
    div[data-testid="stAlert"] {
        border-radius: 24px !important;
        padding: 24px 32px !important;
        border: none !important;
    }
    div[data-testid="stAlert"] > div {
        color: var(--ink) !important;
    }
    div[data-testid="stAlert"] p,
    div[data-testid="stAlert"] span,
    div[data-testid="stAlert"] div {
        color: var(--ink) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 18px !important;
        font-weight: 320 !important;
    }
    /* Info: cream block */
    div[data-baseweb="notification"][kind="info"],
    div.stAlert [data-testid="stNotificationContentInfo"] {
        background-color: var(--block-cream) !important;
        color: var(--ink) !important;
    }
    /* Success: mint block */
    div[data-baseweb="notification"][kind="positive"],
    div.stAlert [data-testid="stNotificationContentSuccess"] {
        background-color: var(--block-mint) !important;
        color: var(--ink) !important;
    }
    /* Warning: coral block */
    div[data-baseweb="notification"][kind="warning"],
    div.stAlert [data-testid="stNotificationContentWarning"] {
        background-color: var(--block-coral) !important;
        color: var(--ink) !important;
    }
    /* Error: pink block */
    div[data-baseweb="notification"][kind="negative"],
    div.stAlert [data-testid="stNotificationContentError"] {
        background-color: var(--block-pink) !important;
        color: var(--ink) !important;
    }

    /* Ensure color-block children inherit color */
    .color-block-lime *, .color-block-lilac *, .color-block-mint *,
    .color-block-coral *, .color-block-cream *, .color-block-navy * {
        color: inherit !important;
    }
    .color-block-navy, .color-block-navy * {
        color: var(--inverse-ink) !important;
    }

    /* Streamlit spinner text fix */
    .stSpinner > div {
        color: var(--ink) !important;
    }

    /* File uploader text visibility */
    div[data-testid="stFileUploader"] label,
    div[data-testid="stFileUploader"] span,
    div[data-testid="stFileUploader"] p,
    div[data-testid="stFileUploader"] small {
        color: var(--ink) !important;
    }

    /* Selectbox label and text */
    div[data-testid="stSelectbox"] * {
        color: var(--ink) !important;
    }

    /* Selectbox dropdown menu item styling */
    div[data-baseweb="popover"] *,
    div[data-baseweb="menu"] * {
        color: var(--ink) !important;
    }


    /* Download button styling as pill */
    div[data-testid="stDownloadButton"] button {
        border-radius: 50px !important;
        font-size: 18px !important;
        font-weight: 480 !important;
        padding: 8px 20px !important;
        background: var(--canvas) !important;
        color: var(--ink) !important;
        border: 1px solid var(--hairline) !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Ensure all Streamlit markdown text is visible */
    div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stMarkdownContainer"] span,
    div[data-testid="stMarkdownContainer"] div {
        color: var(--ink) !important;
    }

    /* Fix progress bar text */
    .stProgress > div > div {
        background-color: var(--ink) !important;
    }
</style>
"""


def inject_design_css():
    import streamlit as st
    st.markdown(DESIGN_CSS, unsafe_allow_html=True)

