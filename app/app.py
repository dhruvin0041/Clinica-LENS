import streamlit as st
import os
import sys
import time
import requests
import base64
from io import BytesIO
from PIL import Image

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Clinica-LENS | Enterprise Diagnostic Assistant", layout="wide")

# Authentication Helper
def login(username, password):
    try:
        response = requests.post(f"{API_URL}/token", data={"username": username, "password": password})
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

# Session State Initialization
if "token" not in st.session_state:
    st.session_state.token = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar Login
st.sidebar.title("🔐 Access Control")
if not st.session_state.token:
    with st.sidebar.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            token_data = login(username, password)
            if token_data:
                st.session_state.token = token_data["access_token"]
                st.sidebar.success("Logged in successfully!")
                st.rerun()
            else:
                st.sidebar.error("Invalid credentials.")
else:
    st.sidebar.success(f"Authenticated")
    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.rerun()

st.title("🏥 Clinica-LENS")
st.markdown("### Enterprise Explainable Multimodal Diagnostic Assistant")

if not st.session_state.token:
    st.warning("Please login from the sidebar to access diagnostic features.")
    st.stop()

st.info("Upload medical scans for asynchronous structured diagnosis, temporal analysis, and VQA.")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("Input Data")
    
    tab_current, tab_prior = st.tabs(["Current Scan", "Prior Scan (Optional)"])
    
    with tab_current:
        uploaded_file = st.file_uploader("Upload Current X-ray (PNG/JPG/DICOM)", type=["png", "jpg", "jpeg", "dcm"], key="current_scan")
        window_center = None
        window_width = None
        
        if uploaded_file:
            st.image(uploaded_file, caption="Current Scan Preview", use_container_width=True)

    with tab_prior:
        prior_file = st.file_uploader("Upload Prior X-ray (Optional)", type=["png", "jpg", "jpeg", "dcm"], key="prior_scan")
        if prior_file:
            st.image(prior_file, caption="Prior Scan", use_container_width=True)

    clinical_text = st.text_area("Patient Symptoms & Clinical Notes", placeholder="e.g., Persistent cough, fever for 3 days, decreased breath sounds in right lower lobe...")

    if st.button("Generate Advanced Diagnosis"):
        if uploaded_file and clinical_text:
            with st.spinner("Submitting to Enterprise Pipeline..."):
                headers = {"Authorization": f"Bearer {st.session_state.token}"}
                files = {"image": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                if prior_file:
                    files["prior_image"] = (prior_file.name, prior_file.getvalue(), prior_file.type)
                
                data = {"clinical_notes": clinical_text}
                
                try:
                    response = requests.post(f"{API_URL}/predict", files=files, data=data, headers=headers)
                    if response.status_code == 401:
                        st.session_state.token = None
                        st.error("Session expired. Please login again.")
                        st.rerun()
                    
                    response.raise_for_status()
                    job_data = response.json()
                    job_id = job_data["job_id"]
                    st.session_state["last_job_id"] = job_id
                    
                    placeholder = st.empty()
                    status = "PENDING"
                    while status == "PENDING":
                        placeholder.text(f"Processing... Job ID: {job_id}")
                        time.sleep(2)
                        status_resp = requests.get(f"{API_URL}/status/{job_id}", headers=headers)
                        status_resp.raise_for_status()
                        status_data = status_resp.json()
                        status = status_data["status"]
                        
                        if status == "SUCCESS":
                            st.session_state['results'] = status_data["result"]
                            placeholder.success("Analysis Complete!")
                            st.rerun()
                        elif status == "FAILURE":
                            placeholder.error(f"Job Failed: {status_data.get('error', 'Unknown error')}")
                            break
                            
                except Exception as e:
                    st.error(f"API Error: {str(e)}")
        else:
            st.error("Current scan and clinical notes are required.")

with col2:
    st.header("Diagnostic Dashboard")
    if 'results' in st.session_state:
        results = st.session_state['results']
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            pred_label = "Positive" if results['prediction'] == 1 else "Negative"
            st.metric("Final Prediction", pred_label)
            st.caption(f"Confidence: {results['mean_probability']*100:.1f}% ± {results['uncertainty']*100:.1f}%")
        
        with col_res2:
            prog = results['progression_score']
            prog_label = "Stable"
            if prog > 0.3: prog_label = "Progression"
            elif prog < -0.3: prog_label = "Improvement"
            st.metric("Temporal Progression", prog_label, delta=f"{prog:.2f}")

        shift = results['prob_shift'] * 100
        st.markdown(f"🧠 **Counterfactual Analysis:** If the highlighted regions were normal, the probability of the diagnosis would shift by **{shift:+.1f}%**.")

        st.subheader("Spatial Attention (Grad-CAM)")
        if "heatmap_b64" in results and results["heatmap_b64"]:
            heatmap_bytes = base64.b64decode(results["heatmap_b64"])
            heatmap_img = Image.open(BytesIO(heatmap_bytes))
            st.image(heatmap_img, caption="High-Attribution Feature Regions", use_container_width=True)
        
        st.subheader("Structured Radiology Report")
        st.markdown("#### Findings")
        st.info(results['findings'])
        st.markdown("#### Impression")
        st.success(results['impression'])
        
        st.divider()
        st.subheader("Conversational VQA (Chat with Scan)")
        st.warning("VQA is currently under migration to Enterprise API. Please check back soon.")

        # Phase 4: HITL Feedback
        st.divider()
        st.subheader("🏥 Clinical Feedback (HITL)")
        with st.form("feedback_form"):
            rating = st.slider("Rate AI Diagnostic Accuracy (1-5)", 1, 5, 5)
            override = st.text_area("Radiologist Override / Corrected Findings (if any)", placeholder="Enter corrections here...")
            comments = st.text_input("General Comments")
            submit_feedback = st.form_submit_button("Submit Clinical Feedback")
            
            if submit_feedback:
                try:
                    headers = {"Authorization": f"Bearer {st.session_state.token}"}
                    fb_data = {
                        "job_id": st.session_state.get("last_job_id", "unknown"),
                        "rating": rating,
                        "comments": comments,
                        "radiologist_override": override
                    }
                    fb_resp = requests.post(f"{API_URL}/feedback", json=fb_data, headers=headers)
                    fb_resp.raise_for_status()
                    st.success("Thank you! Your feedback has been recorded for model optimization.")
                except Exception as e:
                    st.error(f"Feedback Submission Error: {str(e)}")
    else:
        st.write("Dashboard will populate after analysis.")

st.sidebar.header("System Admin")
if st.sidebar.button("Reset Session"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
