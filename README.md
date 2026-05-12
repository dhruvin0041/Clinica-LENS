# Clinica-LENS: Professional Multimodal Clinical Diagnostic Partner

![Status](https://img.shields.io/badge/Status-Professional--Edition-gold) ![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white) ![Next.js](https://img.shields.io/badge/Next.js-14-black?logo=next.js&logoColor=white) ![PyTorch](https://img.shields.io/badge/PyTorch-2.x-red?logo=pytorch) ![FastAPI](https://img.shields.io/badge/FastAPI-Production-009688?logo=fastapi&logoColor=white)

Clinica-LENS is a professional-grade Medical AI assistant designed to transform radiology workflows. It integrates state-of-the-art computer vision, hybrid RAG, and rigorous clinical safety mechanisms to act as a transparent and verifiable diagnostic partner.

## 🌟 Advanced Clinical Features

### 🧠 Domain-Specific Intelligence
*   **Vision (CheXNet):** DenseNet121 backbone optimized for chest radiography.
*   **Text (SapBERT):** SapBERT embeddings for deep medical entity alignment.
*   **Advanced RAG:** **BGE Cross-Encoder Re-ranking** for high-precision literature retrieval.

### 🔬 Multi-Modal Reasoning
*   **Transformer Fusion:** Multimodal Transformer with Cross-Attention.
*   **Conversational VQA:** Stateful Chat-with-Scan interface for image-grounded interrogation.
*   **Clinical Inpainting:** **OpenCV-based Counterfactuals** that fill abnormal regions with realistic "normal" textures for "What-If" analysis.

### 🛡️ Safety & Clinical Rigor
*   **Uncertainty Estimation:** Monte Carlo (MC) Dropout confidence intervals.
*   **Conformal Prediction:** Formal statistical coverage guarantees for diagnostic sets.
*   **NLI Fact-Checking:** **Natural Language Inference (NLI)** guardrails that verify every claim against peer-reviewed literature.
*   **Hybrid Search:** Combined semantic (FAISS) and keyword (BM25) retrieval.

### 🏥 Professional Radiology Workflow
*   **Longitudinal Analysis:** Siamese network for Temporal Progression Scoring.
*   **Native DICOM Support:** Support for 16-bit high-bit depth data with windowing controls.
*   **Structured Reporting:** Automated generation of formal radiology reports.
*   **Production API:** **FastAPI-powered** backend for enterprise integration.

## 🏗️ Technical Architecture

1.  **Vision Layer:** DenseNet121 feature map extractor.
2.  **Language Layer:** SapBERT embeddings + BGE Re-ranking.
3.  **Fusion Layer:** Transformer-based sequence interaction.
4.  **Verification Layer:** NLI-based fact-checking and Conformal Prediction.
5.  **Explainability:** Grad-CAM + Inpainted Counterfactuals.

## 🚀 Getting Started

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/dhruvin0041/Clinica-LENS
   cd Clinica-LENS
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage
1. **Literature Setup:** Place medical PDFs in `data/medical_literature/`.
2. **Run the Dashboard:**
   ```bash
   streamlit run app/app.py
   ```
3. **Run the Production API:**
   ```bash
   python src/api.py
   ```

## 📁 Project Structure

* `app/app.py`: Streamlit dashboard with VQA and DICOM controls.
* `src/api.py`: Production-grade FastAPI backend.
* `src/models.py`: Vision, Fusion, and Temporal Siamese architectures.
* `src/rag_pipeline.py`: SapBERT RAG with BGE Re-ranking and NLI verification.
* `src/pipeline.py`: Unified orchestrator with Conformal Prediction.
* `src/xai.py`: Grad-CAM and Inpainting counterfactuals.
* `tests/`: Automated test suite for core logic.

## 🎓 Professional Edition
This project demonstrates expertise in **Multimodal Medical AI**, **Clinical Decision Support**, and **Safety-Critical Machine Learning**. It is built for transparency, statistical rigor, and enterprise-ready deployment.

---
*Disclaimer: This is a professional research prototype for portfolio purposes and is not intended for real-world clinical diagnosis.*
