# Graph Report - .  (2026-05-12)

## Corpus Check
- Corpus is ~19,828 words - fits in a single context window. You may not need a graph.

## Summary
- 93 nodes · 113 edges · 14 communities detected
- Extraction: 69% EXTRACTED · 31% INFERRED · 0% AMBIGUOUS · INFERRED: 35 edges (avg confidence: 0.65)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]

## God Nodes (most connected - your core abstractions)
1. `MedicalRAG` - 17 edges
2. `ClinicaLENSPipeline` - 13 edges
3. `ClinicaVisionModel` - 12 edges
4. `ClinicaFusionModel` - 8 edges
5. `Clinica-LENS` - 5 edges
6. `DiagnosisResponse` - 4 edges
7. `predict()` - 4 edges
8. `Unified Upgraded Pipeline for Clinica-LENS.     Orchestrates CheXNet Vision, Sa` - 4 edges
9. `Phase 4: Support DICOM windowing for high-bit depth images.` - 4 edges
10. `Runs the multimodal prediction pipeline with Temporal analysis, Counterfactuals,` - 4 edges

## Surprising Connections (you probably didn't know these)
- `Radiographic Findings of CAP` --conceptually_related_to--> `ClinicaVisionModel`  [INFERRED]
  data/medical_literature/cap_summary.txt → src/models.py
- `Generates Grad-CAM heatmaps for a given model and input image.          Args:` --uses--> `ClinicaVisionModel`  [INFERRED]
  C:\DATA SCIENCE\Project\Clinica-LENS\src\xai.py → src/models.py
- `Overlays a heatmap onto an image.` --uses--> `ClinicaVisionModel`  [INFERRED]
  C:\DATA SCIENCE\Project\Clinica-LENS\src\xai.py → src/models.py
- `Phase 3 Upgrade: Generates a counterfactual image using OpenCV Inpainting.` --uses--> `ClinicaVisionModel`  [INFERRED]
  C:\DATA SCIENCE\Project\Clinica-LENS\src\xai.py → src/models.py
- `Model Architectures` --implements--> `Vision Layer`  [INFERRED]
  src/models.py → README.md

## Communities

### Community 0 - "Community 0"
Cohesion: 0.23
Nodes (9): ClinicaFusionModel, Combines Vision and Text embeddings to predict diagnosis, ClinicaVisionModel, Uses pre-trained ResNet/ViT for feature embeddings, ClinicaLENSPipeline, Phase 4: Conversational VQA., Unified Upgraded Pipeline for Clinica-LENS.     Orchestrates CheXNet Vision, Sa, Phase 4: Support DICOM windowing for high-bit depth images. (+1 more)

### Community 1 - "Community 1"
Cohesion: 0.15
Nodes (15): BGE Cross-Encoder, CheXNet, Clinica-LENS, Conformal Prediction, Fusion Layer, Language Layer, Model Architectures, NLI Fact-Checking (+7 more)

### Community 2 - "Community 2"
Cohesion: 0.17
Nodes (6): MedicalRAG, Phase 2: NLI-based Fact Checking., Generates a verified structured report., Upgraded Retrieval-Augmented Generation pipeline for Clinica-LENS.     Uses Sap, Phase 4: Conversational Visual QA loop., Loads PDFs, splits them, and creates Hybrid Search indexes.

### Community 3 - "Community 3"
Cohesion: 0.24
Nodes (6): DiagnosisResponse, health(), predict(), BaseModel, Initializes a local LLM and the RAG chain., Loads existing FAISS and reconstructs BM25 index from stored docs.

### Community 4 - "Community 4"
Cohesion: 0.28
Nodes (7): Streamlit Dashboard, generate_counterfactual(), get_grad_cam(), overlay_heatmap(), Overlays a heatmap onto an image., Phase 3 Upgrade: Generates a counterfactual image using OpenCV Inpainting., Generates Grad-CAM heatmaps for a given model and input image.          Args:

### Community 5 - "Community 5"
Cohesion: 0.48
Nodes (5): test_fusion_model_forward(), test_pipeline_initialization(), test_rag_initialization(), test_temporal_model_forward(), test_vision_model_forward()

### Community 6 - "Community 6"
Cohesion: 0.4
Nodes (5): Clinical Inpainting, Explainability Layer, Grad-CAM, Rationale for Clinical Inpainting, XAI Module

### Community 7 - "Community 7"
Cohesion: 0.67
Nodes (3): Community-Acquired Pneumonia (CAP), CURB-65 Severity Assessment, Radiographic Findings of CAP

### Community 8 - "Community 8"
Cohesion: 1.0
Nodes (3): Agent Instructions, Project Instructions, Graphify Knowledge Graph

### Community 17 - "Community 17"
Cohesion: 1.0
Nodes (1): Chest X-ray: Bacterial Pneumonia

### Community 18 - "Community 18"
Cohesion: 1.0
Nodes (1): Chest X-ray: Viral Pneumonia

### Community 19 - "Community 19"
Cohesion: 1.0
Nodes (1): Dependencies

### Community 20 - "Community 20"
Cohesion: 1.0
Nodes (1): FastAPI Backend

### Community 21 - "Community 21"
Cohesion: 1.0
Nodes (1): Streamlit Dashboard

## Knowledge Gaps
- **24 isolated node(s):** `Uses pre-trained ResNet/ViT for feature embeddings`, `Combines Vision and Text embeddings to predict diagnosis`, `Upgraded Retrieval-Augmented Generation pipeline for Clinica-LENS.     Uses Sap`, `Loads PDFs, splits them, and creates Hybrid Search indexes.`, `Loads existing FAISS and reconstructs BM25 index from stored docs.` (+19 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 17`** (1 nodes): `Chest X-ray: Bacterial Pneumonia`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 18`** (1 nodes): `Chest X-ray: Viral Pneumonia`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 19`** (1 nodes): `Dependencies`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 20`** (1 nodes): `FastAPI Backend`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 21`** (1 nodes): `Streamlit Dashboard`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `MedicalRAG` connect `Community 2` to `Community 0`, `Community 3`, `Community 5`?**
  _High betweenness centrality (0.186) - this node is a cross-community bridge._
- **Why does `ClinicaLENSPipeline` connect `Community 0` to `Community 2`, `Community 3`, `Community 4`, `Community 5`?**
  _High betweenness centrality (0.140) - this node is a cross-community bridge._
- **Why does `ClinicaVisionModel` connect `Community 0` to `Community 4`, `Community 5`, `Community 7`?**
  _High betweenness centrality (0.120) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `MedicalRAG` (e.g. with `ClinicaLENSPipeline` and `Unified Upgraded Pipeline for Clinica-LENS.     Orchestrates CheXNet Vision, Sa`) actually correct?**
  _`MedicalRAG` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `ClinicaLENSPipeline` (e.g. with `DiagnosisResponse` and `ClinicaVisionModel`) actually correct?**
  _`ClinicaLENSPipeline` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `ClinicaVisionModel` (e.g. with `ClinicaLENSPipeline` and `Unified Upgraded Pipeline for Clinica-LENS.     Orchestrates CheXNet Vision, Sa`) actually correct?**
  _`ClinicaVisionModel` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `ClinicaFusionModel` (e.g. with `ClinicaLENSPipeline` and `Unified Upgraded Pipeline for Clinica-LENS.     Orchestrates CheXNet Vision, Sa`) actually correct?**
  _`ClinicaFusionModel` has 7 INFERRED edges - model-reasoned connections that need verification._