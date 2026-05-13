# Project Instructions: Clinica-LENS
**Repository:** https://github.com/dhruvin0041/Clinica-LENS

## Foundational Mandates

### 💎 Clinical Excellence & Branding
- **No Numerical Ratings:** NEVER include numerical ratings (e.g., 100/100, 92/100) or arbitrary "Gold Standard" branding in any documentation or code. Focus exclusively on technical and clinical capabilities.
- **Safety First:** This is an enterprise-grade Software as a Medical Device (SaMD). All changes MUST maintain clinical probability calibration and uncertainty estimation.
- **Regulatory Integrity:** Maintain the `regulatory/` directory. All architectural changes must be reflected in the Technical File and Risk Management Plan.
- **Institutional Isolation:** Never compromise multi-tenant logic. Institutional data boundaries are inviolable.

### 🔗 Networking & Interoperability
- **Active PACS Logic:** Use `src/dicom_client.py` for active study retrieval. Ensure `C-FIND` and `C-MOVE` operations are optimized for hospital network bandwidth.
- **FHIR Write-Back:** Maintain active write-back capabilities for EHR synchronization.

### 🚀 Operational Mandates
- **Immediate Sync:** Every modification MUST be followed by a git commit and an immediate push to `https://github.com/dhruvin0041/Clinica-LENS`.
- **Graphify:** Keep the knowledge graph current (`graphify update`).
- **Distributed Reliability:** Validate changes against both `docker-compose.yml` and the `k8s/` manifests.
- **Audit Trails:** Ensure every active network request (FHIR, DICOM, API) is recorded in the tenant-aware `audit.log`.
- **Probability Calibration:** If models are updated, recalibrate the `ClinicalCalibrator` in `src/calibration.py` using hardware-agnostic validation sets.
