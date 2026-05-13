<div align="center">
# 🏥 Clinica-LENS
**The Unified Multimodal Clinical Diagnostic Platform**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch 2.0+](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C.svg)](https://pytorch.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-009688.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Native-326CE5.svg)](https://kubernetes.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![EHR Integration](https://img.shields.io/badge/EHR-FHIR_Full_Integration-blueviolet.svg?style=for-the-badge)](https://github.com/dhruvin0041/Clinica-LENS)
[![Regulatory Ready](https://img.shields.io/badge/Compliance-FDA_510(k)_Ready-success.svg?style=for-the-badge)](https://github.com/dhruvin0041/Clinica-LENS)
[![DICOM Support](https://img.shields.io/badge/Imaging-DICOM_%7C_DICOMweb-orange.svg?style=for-the-badge)](https://github.com/dhruvin0041/Clinica-LENS)

[Overview](#-overview) • [Key Pillars](#-key-pillars) • [Architecture](#-architecture) • [Getting Started](#-getting-started) • [Regulatory](#-regulatory) • [MLOps](#-mlops)

</div>

---

## 🌟 Overview

**Clinica-LENS (Longitudinal Explainable Network System)** is a diagnostic platform engineered for hospital networks. It is a clinical production system that unifies vision, text, and temporal analysis with statistical reliability and active medical infrastructure integration.


---

## 💎 Key Pillars

### 🔗 Active Medical Interoperability
*   **Full FHIR Integration:** Active write-back of AI-generated `DiagnosticReport` resources to hospital EHRs.
*   **Active PACS SCU:** Integrated DICOM Client capable of **C-FIND** and **C-MOVE** to automatically retrieve historical patient scans.
*   **Modern DICOMweb:** Full WADO-RS and QIDO-RS stubs for cloud-native medical imaging workflows.

### 🛡️ Regulatory & Clinical Safety
*   **Regulatory Ready:** Comprehensive framework for **FDA 510(k)** and **CE-MDR** submission, including CER and Risk Management plans.
*   **Clinical Calibration:** Advanced **Platt Scaling** layer ensuring AI confidence scores are statistically aligned with real-world clinical probabilities.
*   **Multi-Tenant Isolation:** Institutional-level data and log separation for global hospital chains.

### ⚡ Distributed High-Scale Infrastructure
*   **Async Task Queue:** Decoupled inference processing using Celery & Redis.
*   **Kubernetes & Triton:** Production manifests for global scaling and optimized serving via NVIDIA Triton.

### 🧠 Deep Explainability (XAI)
*   **Reasoning-as-a-Service:** Combination of Grad-CAM spatial heatmaps, Counterfactual "What-If" analysis, and Longitudinal progression scoring.

---

## 🏗 Architecture

Clinica-LENS follows a "Clinical Mesh" architecture:
- **Frontend:** Streamlit-based High-Fidelity Dashboard.
- **API Gateway:** Multi-tenant FastAPI with OAuth2 and Prometheus monitoring.
- **Inference Workers:** Distributed Celery nodes optimized for multimodal processing.
- **Networking Tier:** Active DICOM SCU (Client) and SCP (Listener) for PACS integration.
- **Regulatory Tier:** Integrated documentation and compliance monitoring.

---

## 📋 Regulatory Documentation

The system includes pre-configured compliance templates in the `regulatory/` directory:
- **Clinical Evaluation Report (CER):** Mapping AI performance to clinical standards.
- **Risk Management Plan:** ISO 14971 compliant hazard analysis and mitigation tracking.
- **Technical File:** Architectural documentation for certification submission.

---

## 🚦 Getting Started

### Launch Distributed Stack
```bash
docker-compose up --build
```

### Access Ports
*   **UI Dashboard:** `http://localhost:8501`
*   **Enterprise API:** `http://localhost:8000`
*   **PACS Client/Listener:** `localhost:11112`
*   **Metrics:** `http://localhost:8000/metrics`

---

<div align="center">

**The Future of Clinical AI, Today.**  
Developed by [dhruvin0041](https://github.com/dhruvin0041)

</div>
