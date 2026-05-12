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
st.markdown("### Explainable Multimodal Diagnostic Assistant")
st.info("Upload a medical image (e.g., Chest X-ray) and provide clinical symptoms to get an AI-assisted diagnosis.")

@st.cache_resource
def load_pipeline():
    pipeline = ClinicaLENSPipeline()
    # For demo purposes, we can try to setup the LLM here or let the user do it
    # We'll assume the user might need to ingest documents first
    return pipeline

pipeline = load_pipeline()

col1, col2 = st.columns([1, 1])

with col1:
    st.header("Input Data")
    uploaded_file = st.file_uploader("Upload Chest X-ray (PNG/JPG)", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
        
    clinical_text = st.text_area("Patient Symptoms & Clinical Notes", placeholder="e.g., Persistent cough, fever for 3 days, decreased breath sounds in right lower lobe...")

    if st.button("Generate Diagnosis"):
        if uploaded_file and clinical_text:
            with st.spinner("Analyzing multimodal data..."):
                # Save uploaded file temporarily
                temp_path = "temp_image.png"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # We need to make sure RAG is ready
                # For this portfolio piece, we'll try to load existing DB or inform user
                pipeline.rag_engine.load_vector_db()
                # pipeline.rag_engine.setup_llm() # This is heavy, maybe do it once
                
                # Check if QA chain is ready
                if not pipeline.rag_engine.qa_chain:
                    st.warning("RAG QA Chain is not initialized. Please ensure medical literature is ingested and LLM is setup.")
                    # Attempt to setup if not done
                    pipeline.rag_engine.setup_llm()
                
                results = pipeline.predict(temp_path, clinical_text)
                
                st.session_state['results'] = results
                st.session_state['temp_path'] = temp_path
        else:
            st.error("Please provide both an image and clinical notes.")

with col2:
    st.header("Diagnostic Results")
    if 'results' in st.session_state:
        results = st.session_state['results']
        
        # 1. Prediction Probabilities
        st.subheader("Final Prediction")
        pred_label = "Positive" if results['prediction'] == 1 else "Negative"
        st.metric(label="Predicted Class", value=pred_label)
        
        # 2. XAI Visualization
        st.subheader("Visual Explanation (Grad-CAM)")
        combined_img = overlay_heatmap(st.session_state['temp_path'], results['heatmap'])
        st.image(combined_img, caption="Heatmap highlighting regions of interest", use_container_width=True)
        
        # 3. RAG Explanation
        st.subheader("Clinical Explanation (RAG-Grounded)")
        st.write(results['rag_explanation'])
        
        if results['rag_sources']:
            with st.expander("View Sources"):
                for source in results['rag_sources']:
                    st.write(f"- {source}")
    else:
        st.write("Results will appear here after analysis.")

st.sidebar.header("System Configuration")
if st.sidebar.button("Ingest Medical Literature"):
    with st.spinner("Processing PDFs in data/medical_literature..."):
        pipeline.rag_engine.ingest_documents()
        st.sidebar.success("Ingestion complete!")

if st.sidebar.button("Setup LLM"):
    with st.spinner("Loading LLM (TinyLlama)..."):
        pipeline.rag_engine.setup_llm()
        st.sidebar.success("LLM Ready!")
