import streamlit as st

def apply_pro_max_theme():
    st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    :root {
        --bg: #FFFFFF;
        --bg-secondary: #F8FAFC;
        --text-primary: #0F172A;
        --text-secondary: #64748B;
        --border: #E2E8F0;
        --accent: #2563EB;
        --success: #10B981;
        --warning: #F59E0B;
        --error: #EF4444;
        --radius: 12px;
        --radius-sm: 8px;
        --shadow-sm: 0 1px 2px 0 rgba(0,0,0,0.05);
        --shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);
    }

    .stApp {
        background-color: var(--bg-secondary);
        color: var(--text-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Hide default Streamlit clutter */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
        letter-spacing: -0.02em !important;
        font-weight: 600 !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: var(--bg) !important;
        border-right: 1px solid var(--border) !important;
    }

    /* Inputs */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: var(--radius-sm) !important;
        border: 1px solid var(--border) !important;
        background-color: var(--bg) !important;
        color: var(--text-primary) !important;
        box-shadow: var(--shadow-sm) !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
    }

    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 1px var(--accent) !important;
    }

    /* Buttons */
    .stButton>button {
        background-color: var(--bg) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        box-shadow: var(--shadow-sm) !important;
        padding: 0.5rem 1rem !important;
    }

    .stButton>button:hover {
        border-color: var(--text-secondary) !important;
        background-color: var(--bg-secondary) !important;
    }

    .stButton>button[kind="primary"] {
        background-color: var(--accent) !important;
        color: #FFFFFF !important;
        border: none !important;
        box-shadow: var(--shadow) !important;
    }

    .stButton>button[kind="primary"]:hover {
        opacity: 0.9;
        transform: translateY(-1px);
    }

    /* Cards / Metrics */
    div[data-testid="stMetric"] {
        background-color: var(--bg);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.25rem;
        box-shadow: var(--shadow-sm);
    }
    div[data-testid="stMetricValue"] {
        color: var(--text-primary);
        font-weight: 700;
        font-size: 1.875rem;
    }
    div[data-testid="stMetricDelta"] {
        font-weight: 500;
        font-size: 0.875rem;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        border-bottom: 1px solid var(--border);
        padding-bottom: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding-top: 12px;
        padding-bottom: 12px;
        color: var(--text-secondary);
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        color: var(--text-primary) !important;
        border-bottom: 2px solid var(--accent) !important;
        background-color: transparent !important;
    }

    /* Uploader */
    [data-testid="stFileUploader"] > div {
        background-color: var(--bg);
        border-radius: var(--radius);
        border: 1px dashed var(--border);
        padding: 2rem;
        transition: all 0.2s ease;
    }
    [data-testid="stFileUploader"] > div:hover {
        border-color: var(--accent);
        background-color: var(--bg-secondary);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        font-weight: 500 !important;
        color: var(--text-primary) !important;
        background-color: var(--bg) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
    }
    .streamlit-expanderContent {
        border: 1px solid var(--border) !important;
        border-top: none !important;
        border-bottom-left-radius: var(--radius-sm) !important;
        border-bottom-right-radius: var(--radius-sm) !important;
        padding: 16px !important;
        background-color: var(--bg) !important;
    }

    /* Container class for generic custom cards */
    .premium-card {
        border: 1px solid var(--border);
        border-radius: var(--radius);
        background-color: var(--bg);
        padding: 20px;
        box-shadow: var(--shadow-sm);
    }
    
    /* Alerts */
    .stAlert {
        border-radius: var(--radius-sm) !important;
        border: 1px solid var(--border) !important;
    }
</style>
    """, unsafe_allow_html=True)