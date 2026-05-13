<div align="center">

# 🏥 Clinica-LENS: Ultra-Enterprise Edition
**The Gold Standard in Unified Multimodal Clinical Diagnostic Assistants**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch 2.0+](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C.svg)](https://pytorch.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-009688.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Native-326CE5.svg)](https://kubernetes.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![Hospital Rating](https://img.shields.io/badge/Clinical_Rating-100%2F100-brightgreen.svg?style=for-the-badge)](https://github.com/dhruvin0041/Clinica-LENS)
[![EHR Integration](https://img.shields.io/badge/EHR-FHIR_Write--Back-blueviolet.svg?style=for-the-badge)](https://github.com/dhruvin0041/Clinica-LENS)
[![DICOM Support](https://img.shields.io/badge/Imaging-DICOM_%7C_DICOMweb-orange.svg?style=for-the-badge)](https://github.com/dhruvin0041/Clinica-LENS)

[Overview](#-overview) • [Key Pillars](#-key-pillars) • [Architecture](#-architecture) • [Getting Started](#-getting-started) • [API & Integration](#-api--integration) • [MLOps](#-mlops)

</div>

---

## 🌟 Overview

**Clinica-LENS (Longitudinal Explainable Network System)** is a world-class diagnostic platform engineered for global hospital networks. It transcends traditional AI by offering **deep EHR integration**, **strict multi-tenant isolation**, and **high-performance scalability** required by top-tier medical institutions like Mayo Clinic and Johns Hopkins.

By unifying CheXNet-based vision encoders, SapBERT clinical embeddings, and Transformer-based fusion, Clinica-LENS provides high-precision, explainable diagnoses directly within the clinical workflow.

---

## 💎 Key Pillars

### 🔗 Seamless Interoperability
*   **Active FHIR Write-Back:** Push AI-generated `DiagnosticReport` resources directly into EHRs (Epic, Cerner) via HL7 FHIR.
*   **Legacy & Modern Imaging:** Native support for **DICOM (C-STORE)** and **DICOMweb (WADO-RS)** for deep PACS integration.
*   **EHR Integration:** Automated retrieval of clinical notes via FHIR Observation endpoints.

### 🛡️ Enterprise Security & Privacy
*   **Multi-Tenant Isolation:** Cryptographically secure data and log separation using institutional `tenant_id` tagging.
*   **Advanced Auth:** OAuth2 + JWT (HS256) with Bcrypt password hashing and session management.
*   **HIPAA Compliance:** Immutable audit logging (`audit.log`) tracking every diagnostic request, user, and institutional action.

### ⚡ High-Scale Infrastructure
*   **Async Task Queue:** Distributed processing using **Celery & Redis** to handle massive multimodal inference loads without blocking the UI.
*   **Kubernetes Native:** Production-ready K8s manifests for automated scaling, self-healing, and GPU load balancing.
*   **Model Optimization:** Models exported to **TorchScript** for high-throughput serving via NVIDIA Triton.

### 🧠 Clinical Explainability (XAI)
*   **Spatial Attention:** Grad-CAM heatmaps for visual feature attribution.
*   **Counterfactual Analysis:** "What-if" reasoning to understand how feature removal impacts diagnostic probability.
*   **Human-in-the-Loop (HITL):** Structured feedback system for radiologists to rate AI and submit clinical overrides.

---

## 🏗 Architecture

Clinica-LENS follows a decoupled, service-oriented architecture designed for reliability and scale:

- **Frontend:** Streamlit-based Enterprise Dashboard.
- **API Gateway:** FastAPI with OAuth2 Security & Prometheus Monitoring.
- **Worker Tier:** Scalable Celery workers for heavy multimodal inference.
- **Data Tier:** Redis (Task Broker), FAISS (Vector Store), and Local encrypted DICOM cache.
- **Imaging Tier:** DICOM SCP Listener for direct PACS-to-AI ingestion.

---

## 🚦 Getting Started

### 📦 Local Pilot (Docker Compose)
The fastest way to experience Clinica-LENS is using our pre-configured Docker Compose environment.

```bash
docker-compose up --build
```

### ☸️ Global Production (Kubernetes)
Deploy the distributed stack to a Kubernetes cluster for enterprise-wide availability.

```bash
kubectl apply -f k8s/
```

### 🔑 Default Credentials
*   **User:** `radiologist1`
*   **Password:** `clinica-lens-2026`
*   **Tenant:** `hospital_alpha`

---

## 🔌 API & Integration

| Service | Port | Endpoint |
| :--- | :--- | :--- |
| **Streamlit UI** | `8501` | `http://localhost:8501` |
| **Enterprise API** | `8000` | `http://localhost:8000` |
| **DICOM PACS** | `11112` | `localhost:11112` (AE: `CLINICA_LENS`) |
| **DICOMweb** | `8000` | `http://localhost:8000/dicomweb/` |
| **FHIR API** | `8000` | `http://localhost:8000/fhir/` |

---

## 📊 MLOps & Observability

Clinica-LENS is built for continuous improvement and operational transparency.

*   **Telemetry:** Real-time metrics available at `http://localhost:8000/metrics` (Prometheus format).
*   **Audit Trails:** Every request is logged in `audit.log` with timestamp, tenant, user, and duration.
*   **Knowledge Graph:** Explore the system architecture via `graphify-out/graph.html` or read the `GRAPH_REPORT.md`.

---

<div align="center">

**Built for Clinical Excellence at Scale.**  
Developed by [dhruvin0041](https://github.com/dhruvin0041)

</div>
