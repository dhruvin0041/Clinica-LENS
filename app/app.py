import streamlit as st
import torch
import os
import sys

# Add the project root to sys.path to resolve 'src' imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from src.pipeline import ClinicaLENSPipeline
from src.xai import overlay_heatmap

st.set_page_config(page_title="Clinica-LENS | Multimodal Diagnostic Assistant", layout="wide")

st.title("🏥 Clinica-LENS")
st.markdown("### Next-Gen Explainable Multimodal Diagnostic Assistant")
st.info("Upload medical scans (Current & Optional Prior) for structured diagnosis, temporal analysis, and VQA.")

@st.cache_resource
def load_pipeline():
    pipeline = ClinicaLENSPipeline()
    return pipeline

pipeline = load_pipeline()

# Initialize chat history for VQA
if "messages" not in st.session_state:
    st.session_state.messages = []

col1, col2 = st.columns([1, 1])

with col1:
    st.header("Input Data")
    
    tab_current, tab_prior = st.tabs(["Current Scan", "Prior Scan (Optional)"])
    
    with tab_current:
        uploaded_file = st.file_uploader("Upload Current X-ray (PNG/JPG/DICOM)", type=["png", "jpg", "jpeg", "dcm"], key="current_scan")
        window_center = None
        window_width = None
        
        if uploaded_file:
            file_ext = os.path.splitext(uploaded_file.name)[1].lower()
            if file_ext == '.dcm':
                st.info("DICOM windowing controls active.")
                window_center = st.slider("Window Center (Level)", min_value=-1000, max_value=2000, value=40, key="wc")
                window_width = st.slider("Window Width", min_value=1, max_value=4000, value=400, key="ww")
            
            temp_preview_path = f"temp_preview{file_ext}"
            with open(temp_preview_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            preview_img = pipeline.load_and_window_image(temp_preview_path, window_center, window_width)
            st.image(preview_img, caption="Current Scan Preview", use_container_width=True)

    with tab_prior:
        prior_file = st.file_uploader("Upload Prior X-ray (Optional)", type=["png", "jpg", "jpeg", "dcm"], key="prior_scan")
        if prior_file:
            st.image(prior_file, caption="Prior Scan", use_container_width=True)

    clinical_text = st.text_area("Patient Symptoms & Clinical Notes", placeholder="e.g., Persistent cough, fever for 3 days, decreased breath sounds in right lower lobe...")

    if st.button("Generate Advanced Diagnosis"):
        if uploaded_file and clinical_text:
            with st.spinner("Executing Next-Gen Pipeline (Temporal, MC Dropout, Counterfactuals)..."):
                # Save current
                file_ext = os.path.splitext(uploaded_file.name)[1].lower()
                temp_path = f"temp_image{file_ext}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Save prior if exists
                prior_path = None
                if prior_file:
                    prior_ext = os.path.splitext(prior_file.name)[1].lower()
                    prior_path = f"temp_prior{prior_ext}"
                    with open(prior_path, "wb") as f:
                        f.write(prior_file.getbuffer())
                
                pipeline.rag_engine.load_vector_db()
                if not pipeline.rag_engine.qa_chain:
                    pipeline.rag_engine.setup_llm()
                
                # Execute Prediction
                results = pipeline.predict(temp_path, clinical_text, prior_image_path=prior_path, 
                                           window_center=window_center, window_width=window_width, mc_samples=15)
                
                st.session_state['results'] = results
                st.session_state['temp_path'] = temp_path
                # Clear messages when a new diagnosis is generated
                st.session_state.messages = []
        else:
            st.error("Current scan and clinical notes are required.")

with col2:
    st.header("Diagnostic Dashboard")
    if 'results' in st.session_state:
        results = st.session_state['results']
        
        # 1. Prediction & Uncertainty
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            pred_label = "Positive" if results['prediction'] == 1 else "Negative"
            st.metric("Final Prediction", pred_label)
            st.caption(f"Confidence: {results['mean_probability']*100:.1f}% ± {results['uncertainty']*100:.1f}%")
        
        with col_res2:
            # Phase 1: Temporal Score
            prog = results['progression_score']
            prog_label = "Stable"
            if prog > 0.3: prog_label = "Progression"
            elif prog < -0.3: prog_label = "Improvement"
            st.metric("Temporal Progression", prog_label, delta=f"{prog:.2f}")

        # Phase 2: Counterfactual ("What If")
        shift = results['prob_shift'] * 100
        st.markdown(f"🧠 **Counterfactual Analysis:** If the highlighted regions were normal, the probability of the diagnosis would shift by **{shift:+.1f}%**.")

        # 2. XAI Visualization
        st.subheader("Spatial Attention (Grad-CAM)")
        preview_img = pipeline.load_and_window_image(st.session_state['temp_path'], window_center, window_width)
        preview_img.save("temp_overlay_bg.png")
        combined_img = overlay_heatmap("temp_overlay_bg.png", results['heatmap'])
        st.image(combined_img, caption="High-Attribution Feature Regions", use_container_width=True)
        
        # 3. Structured Report (Phase 3)
        st.subheader("Structured Radiology Report")
        st.markdown("#### Findings")
        st.info(results['findings'])
        st.markdown("#### Impression")
        st.success(results['impression'])
        
        # 4. Conversational VQA (Phase 4)
        st.divider()
        st.subheader("Conversational VQA (Chat with Scan)")
        
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask about the heart size, costophrenic angles, or the report..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Consulting literature and image context..."):
                    response = pipeline.chat(prompt)
                    st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    else:
        st.write("Dashboard will populate after analysis.")

st.sidebar.header("System Admin")
if st.sidebar.button("Re-Ingest Literature"):
    with st.spinner("Updating indexes..."):
        pipeline.rag_engine.ingest_documents()
        st.sidebar.success("Indexes Updated.")

if st.sidebar.button("Reset Session"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
