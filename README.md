# Clinica-LENS: Explainable Multimodal Diagnostic Assistant

Clinica-LENS is an advanced Medical AI prototype designed to assist clinicians by combining computer vision and natural language processing for chest radiography analysis. It integrates deep learning-based image feature extraction with Retrieval-Augmented Generation (RAG) to provide diagnostic predictions grounded in peer-reviewed medical literature.

## 🌟 Key Features

*   **Multimodal Fusion:** Integrates ResNet50 vision embeddings with LLM-based text embeddings (using `all-mpnet-base-v2`) to perform binary classification (Positive/Negative diagnosis).
*   **Retrieval-Augmented Generation (RAG):** Uses a FAISS Vector Database to retrieve relevant clinical context from local medical PDFs, providing an LLM-generated explanation grounded in literature.
*   **Explainable AI (XAI):** Implements **Grad-CAM** (via Captum) to generate visual heatmaps, highlighting the specific regions in the Chest X-ray that influenced the model's prediction.
*   **Interactive Dashboard:** A full-stack Streamlit interface for seamless clinical interaction, including document ingestion and real-time diagnostic generation.

## 🏗️ Architecture

1.  **Vision Layer:** ResNet50 backbone (pre-trained on ImageNet) used as a feature encoder.
2.  **Language Layer:** LangChain-powered RAG pipeline using `TinyLlama-1.1B` and `sentence-transformers`.
3.  **Fusion Layer:** A custom neural network that concatenates multimodal embeddings and predicts the clinical outcome.
4.  **Explanation Layer:** Dual-modality explanations via visual heatmaps (Vision) and retrieved clinical context (Text).

## 🚀 Getting Started

### Prerequisites
* Python 3.10+
* 8GB+ RAM (16GB recommended for LLM execution)

### Installation
1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd Clinica-LENS
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install langchain-community langchain-text-splitters
   ```

### Setup
1. **Literature:** Place medical PDFs in `data/medical_literature/`.
2. **Run the Dashboard:**
   ```bash
   streamlit run app/app.py
   ```
3. **Initialize:** Use the sidebar buttons in the app to **Ingest Medical Literature** and **Setup LLM**.

## 📁 Project Structure

* `app/`: Streamlit frontend application.
* `src/models.py`: Vision and Fusion model architectures.
* `src/rag_pipeline.py`: RAG logic and vector store management.
* `src/xai.py`: Grad-CAM implementation.
* `src/pipeline.py`: The unified orchestrator for the system.
* `data/`: Directory for medical literature and images.
* `models/`: Storage for the FAISS index and model weights.

## 🎓 Portfolio Note
This project was developed to demonstrate expertise in **Multimodal Fusion**, **Explainable AI (XAI)**, and **Medical Machine Learning**. It highlights the ability to move beyond "black-box" models by grounding AI predictions in verified medical literature and visual evidence.

---
*Disclaimer: This is a research prototype for portfolio purposes and is not intended for real-world clinical diagnosis.*
