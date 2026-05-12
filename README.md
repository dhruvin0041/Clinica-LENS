# Clinica-LENS: Advanced Multimodal Clinical Diagnostic Partner

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-14-black?logo=next.js&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange?logo=tensorflow)
![PyTorch](https://img.shields.io/badge/PyTorch-2.x-red?logo=pytorch)

Clinica-LENS is a high-fidelity Medical AI assistant designed to transform radiology workflows. It moves beyond simple classification by acting as a collaborative partner, integrating computer vision, natural language processing, and state-of-the-art explainability.

## 🌟 Advanced Clinical Features

### 🧠 Domain-Specific Intelligence
*   **Vision (CheXNet):** Utilizes a **DenseNet121** backbone optimized for chest radiography, capable of detecting subtle clinical markers.
*   **Text (SapBERT):** Leverages **SapBERT** embeddings, providing deep understanding of medical terminology and entity alignment.

### 🔬 Multi-Modal Reasoning
*   **Transformer Fusion:** Employs a **Multimodal Transformer with Cross-Attention**, allowing clinical notes to dynamically guide the vision model's focus.
*   **Conversational VQA:** A stateful **Chat-with-Scan** interface that allows clinicians to interrogate images with natural language questions.

### 🛡️ Safety & Clinical Rigor
*   **Uncertainty Estimation:** Uses **Monte Carlo (MC) Dropout** to provide a confidence interval (±%) for every diagnosis, flagging high-uncertainty cases for manual review.
*   **Hallucination Guardrails:** A self-correction loop that verifies AI claims against peer-reviewed medical literature.
*   **Hybrid Search:** Combines semantic (FAISS) and keyword (BM25) retrieval for zero-miss clinical grounding.

### 🏥 Professional Radiology Workflow
*   **Longitudinal Analysis:** A Siamese network architecture that compares **Current vs. Prior** scans to calculate a **Temporal Progression Score**.
*   **Native DICOM Support:** Support for high-bit depth 16-bit medical data with real-time **Clinical Windowing** (Level/Width) controls.
*   **Structured Reporting:** Automatically generates formal reports with **Findings** and **Impression** sections.
*   **Counterfactual XAI:** "What-If" analysis that quantifies how specific image regions influence the final diagnostic probability.

## 🏗️ Technical Architecture

1.  **Vision Layer:** DenseNet121 feature map extractor.
2.  **Language Layer:** SapBERT embeddings with Ensemble Retrieval (FAISS + BM25).
3.  **Fusion Layer:** Transformer-based sequence encoder.
4.  **Temporal Layer:** Siamese comparison network for progression monitoring.
5.  **Explainability:** Grad-CAM spatial attention + Feature Occlusion counterfactuals.

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
3. **Initialize:** Use the sidebar to **Re-Ingest Literature** and **Setup LLM**.

## 📁 Project Structure

* `app/app.py`: Next-Gen Streamlit dashboard with VQA and DICOM controls.
* `src/models.py`: CheXNet, Transformer Fusion, and Temporal Siamese architectures.
* `src/rag_pipeline.py`: Hybrid search, SapBERT embeddings, and chat history management.
* `src/pipeline.py`: The unified clinical orchestrator.
* `src/xai.py`: Grad-CAM and Counterfactual logic.

## 🎓 Research Prototype
This project demonstrates expertise in **Multimodal Medical AI**, **Clinical Decision Support**, and **Safety-Critical Machine Learning**. It highlights the ability to build AI systems that are transparent, verifiable, and aligned with clinical standards.

---
*Disclaimer: This is a research prototype for portfolio purposes and is not intended for real-world clinical diagnosis.*
