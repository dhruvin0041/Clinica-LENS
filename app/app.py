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
st.markdown("### Upgraded Explainable Multimodal Diagnostic Assistant")
st.info("Upload a medical image (X-ray/DICOM) and provide clinical symptoms for a grounded AI diagnosis.")

@st.cache_resource
def load_pipeline():
    pipeline = ClinicaLENSPipeline()
    return pipeline

pipeline = load_pipeline()

col1, col2 = st.columns([1, 1])

with col1:
    st.header("Input Data")
    uploaded_file = st.file_uploader("Upload Chest X-ray (PNG/JPG/DICOM)", type=["png", "jpg", "jpeg", "dcm"])
    
    window_center = None
    window_width = None
    
    if uploaded_file:
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        # Phase 4: Handle DICOM specifically for the UI
        if file_ext == '.dcm':
            st.info("DICOM file detected. Adjust clinical windowing below.")
            window_center = st.slider("Window Center (Level)", min_value=-1000, max_value=2000, value=40)
            window_width = st.slider("Window Width", min_value=1, max_value=4000, value=400)
            
        # Display the image (using the pipeline's windowing logic for preview)
        temp_preview_path = f"temp_preview{file_ext}"
        with open(temp_preview_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        preview_img = pipeline.load_and_window_image(temp_preview_path, window_center, window_width)
        st.image(preview_img, caption="Preview (Processed)", use_container_width=True)
        
    clinical_text = st.text_area("Patient Symptoms & Clinical Notes", placeholder="e.g., Persistent cough, fever for 3 days, decreased breath sounds in right lower lobe...")

    if st.button("Generate Diagnosis"):
        if uploaded_file and clinical_text:
            with st.spinner("Analyzing multimodal data (MC Dropout Inference)..."):
                file_ext = os.path.splitext(uploaded_file.name)[1].lower()
                temp_path = f"temp_image{file_ext}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                pipeline.rag_engine.load_vector_db()
                if not pipeline.rag_engine.qa_chain:
                    pipeline.rag_engine.setup_llm()
                
                # Phase 4: Pass windowing and mc_samples
                results = pipeline.predict(temp_path, clinical_text, window_center, window_width, mc_samples=15)
                
                st.session_state['results'] = results
                st.session_state['temp_path'] = temp_path
        else:
            st.error("Please provide both an image and clinical notes.")

with col2:
    st.header("Diagnostic Results")
    if 'results' in st.session_state:
        results = st.session_state['results']
        
        # 1. Prediction with Uncertainty (Phase 3)
        st.subheader("Final Prediction & Confidence")
        pred_label = "Positive" if results['prediction'] == 1 else "Negative"
        prob_pct = results['mean_probability'] * 100
        uncert_pct = results['uncertainty'] * 100
        
        color = "red" if results['uncertainty'] > 0.15 else "green"
        st.markdown(f"### Label: **{pred_label}**")
        st.markdown(f"#### Confidence: **{prob_pct:.1f}% ± {uncert_pct:.1f}%**")
        
        if results['uncertainty'] > 0.15:
            st.warning("⚠️ **High Uncertainty detected.** Results should be manually verified by a senior radiologist.")
        else:
            st.success("✅ Confidence levels within standard operating parameters.")
        
        # 2. XAI Visualization (Phase 2: CheXNet Attention)
        st.subheader("Visual Explanation (Spatial Attention)")
        # We need to use the windowed image for the background of the heatmap
        preview_img = pipeline.load_and_window_image(st.session_state['temp_path'], window_center, window_width)
        preview_img.save("temp_overlay_bg.png")
        
        combined_img = overlay_heatmap("temp_overlay_bg.png", results['heatmap'])
        st.image(combined_img, caption="Grad-CAM highlight (Target: Last Dense Block)", use_container_width=True)
        
        # 3. RAG Explanation with Hallucination Guardrail (Phase 5)
        st.subheader("Clinical Grounding")
        
        status = results['rag_status']
        if "SAFE" in status.upper():
            st.caption("🛡️ **Verification Status: Grounded in Literature**")
        else:
            st.error(f"🚨 **Hallucination Warning:** {status}")
            
        st.write(results['rag_explanation'])
        
        if results['rag_sources']:
            with st.expander("View Cited Literature"):
                for source in results['rag_sources']:
                    st.write(f"- {source}")
    else:
        st.write("Results will appear here after analysis.")

st.sidebar.header("System Configuration")
if st.sidebar.button("Ingest Medical Literature"):
    with st.spinner("Building Hybrid Search Indexes..."):
        pipeline.rag_engine.ingest_documents()
        st.sidebar.success("Hybrid Search Ready!")

if st.sidebar.button("Setup LLM"):
    with st.spinner("Loading LLM (TinyLlama)..."):
        pipeline.rag_engine.setup_llm()
        st.sidebar.success("LLM & QA Chain Ready!")
