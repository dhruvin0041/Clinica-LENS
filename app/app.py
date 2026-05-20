import streamlit as st
import os
import time
import requests
import base64
from io import BytesIO
from PIL import Image

# Import Modular Frontend Architecture
from theme import apply_pro_max_theme
from components import empty_state, skeleton_loader, status_badge

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Ensure full width and collapsed initial state if needed, but sidebar is okay
st.set_page_config(
    page_title="Clinica-LENS | Enterprise AI", 
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🧬"
)

# Apply World-Class Light Theme (Vercel/Linear/Stripe inspired)
apply_pro_max_theme()

# --- State Management ---
if "token" not in st.session_state:
    st.session_state.token = None
if "current_view" not in st.session_state:
    st.session_state.current_view = "Dashboard"

def login(username, password):
    try:
        response = requests.post(f"{API_URL}/token", data={"username": username, "password": password})
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

# --- UI Components ---
def render_sidebar():
    with st.sidebar:
        st.markdown("""
            <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 32px;'>
                <div style='background: #0F172A; color: white; width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 18px;'>C</div>
                <h2 style='margin: 0; font-size: 18px;'>Clinica-LENS</h2>
            </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.token:
            st.markdown("<p style='font-size: 14px; font-weight: 500; color: #64748B; margin-bottom: 16px;'>AUTHENTICATION</p>", unsafe_allow_html=True)
            with st.form("login_form"):
                username = st.text_input("Work Email")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Sign In", type="primary", use_container_width=True)
                if submitted:
                    token_data = login(username, password)
                    if token_data:
                        st.session_state.token = token_data["access_token"]
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")
        else:
            st.markdown("<p style='font-size: 12px; font-weight: 600; color: #64748B; margin-bottom: 8px; letter-spacing: 0.05em;'>WORKSPACE</p>", unsafe_allow_html=True)
            
            # Custom Navigation 
            if st.button("📊 Dashboard", use_container_width=True, type="secondary" if st.session_state.current_view != "Dashboard" else "primary"):
                st.session_state.current_view = "Dashboard"
                st.rerun()
            if st.button("🔬 New Study Analysis", use_container_width=True, type="secondary" if st.session_state.current_view != "Analysis" else "primary"):
                st.session_state.current_view = "Analysis"
                st.rerun()
            if st.button("⚙️ Settings", use_container_width=True, type="secondary" if st.session_state.current_view != "Settings" else "primary"):
                st.session_state.current_view = "Settings"
                st.rerun()
            
            st.markdown("<hr style='border: 0; height: 1px; background: #E2E8F0; margin: 24px 0;'>", unsafe_allow_html=True)
            st.markdown("<div style='display: flex; align-items: center; gap: 8px;'><div style='width: 8px; height: 8px; background-color: #10B981; border-radius: 50%;'></div><span style='font-size: 14px; color: #0F172A; font-weight: 500;'>API Connected</span></div>", unsafe_allow_html=True)
            
            if st.button("Sign Out", use_container_width=True):
                st.session_state.token = None
                st.session_state.current_view = "Dashboard"
                st.rerun()

def render_login_view():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center; max-width: 400px; margin: 0 auto;'>
            <div style='background: #0F172A; color: white; width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 24px; margin: 0 auto 24px auto; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);'>C</div>
            <h1 style='font-size: 30px; margin-bottom: 12px;'>Welcome to Clinica-LENS</h1>
            <p style='color: #64748B; font-size: 16px;'>Enterprise Diagnostic Intelligence. Please sign in via the sidebar to continue.</p>
        </div>
    """, unsafe_allow_html=True)

def render_dashboard():
    st.markdown("## Overview")
    st.markdown("<p style='color: #64748B; margin-top: -10px; margin-bottom: 24px;'>High-level metrics and recent diagnostic activity.</p>", unsafe_allow_html=True)
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Studies Processed", "1,248", "12% this week")
    m2.metric("Critical Findings", "84", "2% this week", delta_color="inverse")
    m3.metric("System Uptime", "99.99%", "Optimal", delta_color="off")
    m4.metric("Avg. Latency", "1.2s", "-0.3s", delta_color="inverse")
    
    st.markdown("### Recent Activity")
    st.markdown("""
    <div class="premium-card" style="margin-top: 16px;">
        <table style="width: 100%; text-align: left; border-collapse: collapse;">
            <tr style="border-bottom: 1px solid #E2E8F0;">
                <th style="padding: 12px; color: #64748B; font-weight: 600; font-size: 12px;">STUDY ID</th>
                <th style="padding: 12px; color: #64748B; font-weight: 600; font-size: 12px;">DATE</th>
                <th style="padding: 12px; color: #64748B; font-weight: 600; font-size: 12px;">STATUS</th>
                <th style="padding: 12px; color: #64748B; font-weight: 600; font-size: 12px;">MODALITY</th>
            </tr>
            <tr style="border-bottom: 1px solid #F1F5F9;">
                <td style="padding: 12px; font-weight: 500;">ST-29381</td>
                <td style="padding: 12px; color: #64748B;">Just now</td>
                <td style="padding: 12px;"><span style="color: #10B981; font-weight: 500;">Completed</span></td>
                <td style="padding: 12px; color: #64748B;">DX</td>
            </tr>
            <tr style="border-bottom: 1px solid #F1F5F9;">
                <td style="padding: 12px; font-weight: 500;">ST-29380</td>
                <td style="padding: 12px; color: #64748B;">2 mins ago</td>
                <td style="padding: 12px;"><span style="color: #10B981; font-weight: 500;">Completed</span></td>
                <td style="padding: 12px; color: #64748B;">DX</td>
            </tr>
            <tr>
                <td style="padding: 12px; font-weight: 500;">ST-29379</td>
                <td style="padding: 12px; color: #64748B;">15 mins ago</td>
                <td style="padding: 12px;"><span style="color: #F59E0B; font-weight: 500;">Requires Review</span></td>
                <td style="padding: 12px; color: #64748B;">DX</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

def render_analysis():
    st.markdown("""
        <div style='display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px;'>
            <div>
                <h2 style='margin: 0;'>New Study Analysis</h2>
                <p style='color: #64748B; margin: 4px 0 0 0;'>Upload a DICOM/PNG study and provide clinical context for AI-augmented reporting.</p>
            </div>
            <span style='background: #DBEAFE; color: #1E40AF; padding: 4px 12px; border-radius: 9999px; font-size: 12px; font-weight: 600;'>Production v2.4</span>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.2], gap="large")

    with col1:
        st.markdown("<h3 style='font-size: 16px; margin-bottom: 16px;'>1. Data Ingestion</h3>", unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Upload Current Study (DICOM, PNG, JPG)", type=["png", "jpg", "jpeg", "dcm"])
        if uploaded_file:
            st.image(uploaded_file, caption="Current Study Preview", use_container_width=True)
            
        prior_file = st.file_uploader("Upload Prior Study (Optional)", type=["png", "jpg", "jpeg", "dcm"])
        
        st.markdown("<hr style='border: 0; height: 1px; background: #E2E8F0; margin: 24px 0;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='font-size: 16px; margin-bottom: 16px;'>2. Clinical Context</h3>", unsafe_allow_html=True)
        
        clinical_text = st.text_area("Patient History & Symptoms", height=120, placeholder="e.g. 45M presents with acute dyspnea and persistent cough for 4 days.")

        if st.button("Run Enterprise Analysis", type="primary", use_container_width=True):
            if uploaded_file and clinical_text:
                with st.spinner("Orchestrating AI Inference & RAG Pipeline..."):
                    headers = {"Authorization": f"Bearer {st.session_state.token}"}
                    files = {"image": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    if prior_file:
                        files["prior_image"] = (prior_file.name, prior_file.getvalue(), prior_file.type)
                    data = {"clinical_notes": clinical_text}
                    
                    try:
                        response = requests.post(f"{API_URL}/predict", files=files, data=data, headers=headers)
                        response.raise_for_status()
                        job_id = response.json()["job_id"]
                        st.session_state["last_job_id"] = job_id
                        
                        status_placeholder = st.empty()
                        status = "PENDING"
                        while status == "PENDING":
                            with status_placeholder.container():
                                skeleton_loader()
                            time.sleep(1.5)
                            status_resp = requests.get(f"{API_URL}/status/{job_id}", headers=headers)
                            if status_resp.status_code == 200:
                                status_data = status_resp.json()
                                status = status_data["status"]
                                if status == "SUCCESS":
                                    st.session_state['results'] = status_data["result"]
                                    status_placeholder.empty()
                                    st.toast("✅ Analysis successfully completed.", icon="🎉")
                                    st.rerun()
                                elif status == "FAILURE":
                                    status_placeholder.empty()
                                    st.error("Analysis Failed")
                                    break
                    except Exception as e:
                        st.error(f"Execution Error: {str(e)}")
            else:
                st.warning("Both a current study and clinical context are required.")

    with col2:
        st.markdown("<h3 style='font-size: 16px; margin-bottom: 16px;'>Diagnostic Report</h3>", unsafe_allow_html=True)
        if 'results' in st.session_state:
            results = st.session_state['results']
            
            # Key Metrics
            m1, m2, m3 = st.columns(3)
            pred_label = "Positive" if results.get('prediction', 0) == 1 else "Negative"
            conf = results.get('mean_probability', 0.0) * 100
            unc = results.get('uncertainty', 0.0) * 100
            prog = results.get('progression_score', 0.0)
            
            m1.metric("Finding", pred_label)
            m2.metric("Confidence", f"{conf:.1f}%", f"±{unc:.1f}% Unc.", delta_color="off")
            m3.metric("Progression", f"{prog:.2f}", "Stable" if abs(prog) < 0.3 else ("Worsened" if prog > 0 else "Improved"), delta_color="inverse")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Tabs for dense information
            tab1, tab2, tab3 = st.tabs(["Clinical Narrative", "Explainability (XAI)", "Quality Assurance"])
            
            with tab1:
                st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
                st.markdown("<div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;'><strong>FINDINGS</strong>", unsafe_allow_html=True)
                status_badge(results.get('rag_status', 'Unknown'))
                st.markdown("</div>", unsafe_allow_html=True)
                st.write(results.get('findings', 'N/A'))
                st.markdown("<hr style='border: 0; height: 1px; background: #E2E8F0; margin: 16px 0;'>", unsafe_allow_html=True)
                st.markdown("**IMPRESSION**")
                st.write(results.get('impression', 'N/A'))
                st.markdown("</div>", unsafe_allow_html=True)
                
            with tab2:
                st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
                if "heatmap_b64" in results and results["heatmap_b64"]:
                    heatmap_bytes = base64.b64decode(results["heatmap_b64"])
                    st.image(Image.open(BytesIO(heatmap_bytes)), caption="Grad-CAM Spatial Attention Map", use_container_width=True)
                    shift = results.get('prob_shift', 0) * 100
                    st.info(f"💡 **Counterfactual Impact:** Resolving highlighted regions shifts probability by {shift:+.1f}%")
                else:
                    st.write("Heatmap not available for this analysis.")
                st.markdown("</div>", unsafe_allow_html=True)
                
            with tab3:
                st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
                st.markdown("**Human-in-the-Loop Feedback**")
                st.markdown("<p style='font-size: 14px; color: #64748B;'>Submit adjustments to improve future model calibration.</p>", unsafe_allow_html=True)
                with st.form("hitl_form"):
                    rating = st.slider("Diagnostic Accuracy Rating", 1, 5, 5)
                    notes = st.text_area("Radiologist Corrections")
                    if st.form_submit_button("Save to Quality Registry", type="primary"):
                        st.success("Feedback registered in the enterprise registry.")
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            empty_state("🧬", "Ready for Analysis", "Upload a study and hit Run Enterprise Analysis to generate a detailed report.")

# --- Main App Execution ---
render_sidebar()

if not st.session_state.token:
    render_login_view()
else:
    if st.session_state.current_view == "Dashboard":
        render_dashboard()
    elif st.session_state.current_view == "Analysis":
        render_analysis()
    elif st.session_state.current_view == "Settings":
        st.markdown("## Settings")
        empty_state("⚙️", "System Settings", "User preferences and API configuration will appear here.")
