# Clinica-LENS: Enterprise Edition 🏥

**Unified Multimodal Clinical Diagnostic Assistant**  
*Next-Gen Explainable AI for Radiology and Longitudinal Patient Analysis*

[![Production Ready](https://img.shields.io/badge/Status-Production--Ready-success)](https://github.com/dhruvin0041/Clinica-LENS)
[![Enterprise Architecture](https://img.shields.io/badge/Arch-Distributed--Async-blue)](https://github.com/dhruvin0041/Clinica-LENS)
[![DICOM Supported](https://img.shields.io/badge/Interoperability-DICOM%20%7C%20FHIR-orange)](https://github.com/dhruvin0041/Clinica-LENS)

---

## 🌟 Overview
Clinica-LENS (Longitudinal Explainable Network System) is an enterprise-grade multimodal diagnostic platform designed for top-tier hospital environments. It integrates CheXNet-based vision encoders, SapBERT clinical embeddings, and Transformer-based fusion to provide high-precision, explainable diagnoses from medical scans and clinical notes.

## 🚀 Key Enterprise Features

### 1. High-Performance Infrastructure
*   **Asynchronous Task Queue:** Powered by **Celery & Redis**. Large multimodal inferences are decoupled from the API, ensuring zero-latency user interaction.
*   **Containerized Orchestration:** Full **Docker & Docker-Compose** support for seamless deployment of API, UI, Workers, and Redis.

### 2. Enterprise Security & Compliance
*   **OAuth2 & JWT:** Secure identity management with token-based authentication and hashed credentials.
*   **Audit Logging:** Immutable clinical audit trails (`audit.log`) tracking every diagnostic request and user action for HIPAA compliance.
*   **RBAC Ready:** Built-in Role-Based Access Control logic for clinicians and admins.

### 3. Medical Interoperability
*   **DICOM PACS Integration:** Built-in **DICOM SCP Listener** (`port 11112`) using `pynetdicom`. Push scans directly from hospital imaging hardware.
*   **FHIR/HL7 Ready:** Mock FHIR endpoints for seamless integration with Electronic Health Records (EHR) like Epic and Cerner.
*   **Automated De-identification:** PHI stripping from DICOM headers during ingestion.

### 4. Advanced Clinical XAI & MLOps
*   **Explainable AI (XAI):** Real-time Grad-CAM heatmaps and Counterfactual ("What If") analysis for diagnostic transparency.
*   **Observability:** Integrated **Prometheus** telemetry (`/metrics`) for monitoring system health, latency, and GPU throughput.
*   **Human-in-the-Loop (HITL):** Clinical feedback system allowing radiologists to rate AI accuracy and submit overrides for model fine-tuning.

---

## 🛠 Tech Stack
*   **Backend:** FastAPI, Celery, Redis
*   **Frontend:** Streamlit
*   **Deep Learning:** PyTorch, Torchvision, Transformers (HuggingFace)
*   **Medical Data:** Pydicom, Pynetdicom
*   **RAG:** LangChain, SapBERT, BM25, FAISS
*   **Security:** JOSE (JWT), Passlib (Bcrypt)

---

## 🚦 Getting Started (Docker Compose)

### 1. Prerequisites
*   Docker & Docker Compose installed.

### 2. Launch Services
```bash
docker-compose up --build
```

### 3. Access Ports
*   **Streamlit UI:** `http://localhost:8501` (Login: `radiologist1` / `clinica-lens-2026`)
*   **FastAPI API:** `http://localhost:8000`
*   **DICOM Listener:** `localhost:11112` (AE Title: `CLINICA_LENS`)
*   **Metrics:** `http://localhost:8000/metrics`

---

## 📊 Knowledge Graph
This project maintains a structural knowledge graph for architectural discovery.
*   **Audit Report:** `graphify-out/GRAPH_REPORT.md`
*   **Visualizer:** `graphify-out/graph.html`

---

**Developed for Clinical Excellence.**  
**Repository:** [https://github.com/dhruvin0041/Clinica-LENS](https://github.com/dhruvin0041/Clinica-LENS)
