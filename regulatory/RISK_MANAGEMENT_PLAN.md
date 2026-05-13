# Risk Management Plan (ISO 14971) - Clinica-LENS

## 1. Scope
This plan describes the risk management activities to be performed for the Clinica-LENS system throughout its lifecycle.

## 2. Risk Management Team
- Chief Medical Officer
- Lead AI Engineer
- Quality Assurance Manager
- Regulatory Affairs Specialist

## 3. Risk Assessment Matrix
Severity (S) x Probability (P) = Risk Level (R)

## 4. Identified Hazards & Mitigations

| Hazard | Cause | Severity | Probability | Mitigation | Residual Risk |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **False Negative** | Sub-optimal image quality | High | Low | DICOM Windowing & Uncertainty Estimation (MC Dropout) | Acceptable |
| **Data Breach** | Unauthorized access | High | Very Low | OAuth2, JWT, and Multi-tenant Isolation | Acceptable |
| **Model Drift** | Hardware variance | Medium | Medium | Clinical Probability Calibration Layer | Acceptable |
| **Misinterpretation** | AI "Black Box" | Medium | Low | Spatial Heatmaps (Grad-CAM) and Counterfactuals | Acceptable |

## 5. Post-Market Surveillance
Collection of clinical feedback via the integrated Human-in-the-Loop (HITL) system to identify unforeseen hazards.
