# Graph Report - .  (2026-05-12)

## Corpus Check
- Corpus is ~18,411 words - fits in a single context window. You may not need a graph.

## Summary
- 66 nodes · 91 edges · 8 communities detected
- Extraction: 60% EXTRACTED · 40% INFERRED · 0% AMBIGUOUS · INFERRED: 36 edges (avg confidence: 0.64)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]

## God Nodes (most connected - your core abstractions)
1. `MedicalRAG` - 16 edges
2. `ClinicaVisionModel` - 15 edges
3. `ClinicaFusionModel` - 12 edges
4. `ClinicaLENSPipeline` - 12 edges
5. `ClinicaTemporalModel` - 10 edges
6. `Unified Upgraded Pipeline for Clinica-LENS.     Orchestrates CheXNet Vision, Sa` - 5 edges
7. `Phase 4: Support DICOM windowing for high-bit depth images.` - 5 edges
8. `Runs the multimodal prediction pipeline with Temporal analysis and Counterfactua` - 5 edges
9. `Phase 4: Conversational VQA.` - 5 edges
10. `get_grad_cam()` - 5 edges

## Surprising Connections (you probably didn't know these)
- `Multimodal Fusion Concept` --semantically_similar_to--> `ClinicaFusionModel`  [INFERRED] [semantically similar]
  README.md → C:\DATA SCIENCE\Project\Clinica-LENS\src\models.py
- `RAG Concept` --semantically_similar_to--> `MedicalRAG`  [INFERRED] [semantically similar]
  README.md → C:\DATA SCIENCE\Project\Clinica-LENS\src\rag_pipeline.py
- `Explainable AI (XAI) Concept` --semantically_similar_to--> `get_grad_cam()`  [INFERRED] [semantically similar]
  README.md → C:\DATA SCIENCE\Project\Clinica-LENS\src\xai.py
- `Radiographic Findings of CAP` --conceptually_related_to--> `ClinicaVisionModel`  [INFERRED]
  data/medical_literature/cap_summary.txt → C:\DATA SCIENCE\Project\Clinica-LENS\src\models.py
- `Generates Grad-CAM heatmaps for a given model and input image.          Args:` --uses--> `ClinicaVisionModel`  [INFERRED]
  C:\DATA SCIENCE\Project\Clinica-LENS\src\xai.py → C:\DATA SCIENCE\Project\Clinica-LENS\src\models.py

## Hyperedges (group relationships)
- **Clinica-LENS Core Architecture** — pipeline_clinicalenspipeline, models_clinicavisionmodel, models_clinicafusionmodel, rag_pipeline_medicalrag, xai_get_grad_cam [INFERRED 0.90]

## Communities

### Community 0 - "Community 0"
Cohesion: 0.14
Nodes (8): MedicalRAG, Phase 5: Self-Correction Loop / Hallucination Guardrail., Upgraded Retrieval-Augmented Generation pipeline for Clinica-LENS.     Uses Sap, Generates a verified structured report., Loads PDFs, splits them, and creates Hybrid Search indexes., Loads existing FAISS and reconstructs BM25 index from stored docs., Initializes a local LLM and the RAG chain., RAG Concept

### Community 1 - "Community 1"
Cohesion: 0.18
Nodes (10): Streamlit Dashboard, Runs the multimodal prediction pipeline with Temporal analysis and Counterfactua, Explainable AI (XAI) Concept, generate_counterfactual(), get_grad_cam(), Attribute to sum of embedding to see global features, overlay_heatmap(), Overlays a heatmap onto an image. (+2 more)

### Community 2 - "Community 2"
Cohesion: 0.24
Nodes (6): load_pipeline(), ClinicaTemporalModel, Siamese Network for Longitudinal Analysis.     Compares current vision embeddin, ClinicaLENSPipeline, Unified Upgraded Pipeline for Clinica-LENS.     Orchestrates CheXNet Vision, Sa, Phase 4: Support DICOM windowing for high-bit depth images.

### Community 3 - "Community 3"
Cohesion: 0.2
Nodes (5): ClinicaFusionModel, Combines Vision and Text embeddings to predict diagnosis, Transformer-based Multimodal Fusion Layer.     Uses Cross-Attention to let Text, vision_features: (B, 1024, 7, 7) from DenseNet         text_emb: (B, 768) from, Multimodal Fusion Concept

### Community 4 - "Community 4"
Cohesion: 0.29
Nodes (6): Community-Acquired Pneumonia (CAP), CURB-65 Severity Assessment, Radiographic Findings of CAP, ClinicaVisionModel, Uses pre-trained ResNet/ViT for feature embeddings, Encoder for Medical Images (X-rays) using CheXNet architecture (DenseNet121).

### Community 5 - "Community 5"
Cohesion: 0.5
Nodes (2): Phase 4: Conversational VQA., Phase 4: Conversational Visual QA loop.

### Community 11 - "Community 11"
Cohesion: 1.0
Nodes (1): Chest X-ray: Bacterial Pneumonia

### Community 12 - "Community 12"
Cohesion: 1.0
Nodes (1): Chest X-ray: Viral Pneumonia

## Knowledge Gaps
- **20 isolated node(s):** `Encoder for Medical Images (X-rays) using CheXNet architecture (DenseNet121).`, `Transformer-based Multimodal Fusion Layer.     Uses Cross-Attention to let Text`, `vision_features: (B, 1024, 7, 7) from DenseNet         text_emb: (B, 768) from`, `Siamese Network for Longitudinal Analysis.     Compares current vision embeddin`, `Upgraded Retrieval-Augmented Generation pipeline for Clinica-LENS.     Uses Sap` (+15 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 5`** (4 nodes): `.chat()`, `Phase 4: Conversational VQA.`, `.chat_vqa()`, `Phase 4: Conversational Visual QA loop.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 11`** (1 nodes): `Chest X-ray: Bacterial Pneumonia`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 12`** (1 nodes): `Chest X-ray: Viral Pneumonia`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `MedicalRAG` connect `Community 0` to `Community 1`, `Community 2`, `Community 5`?**
  _High betweenness centrality (0.344) - this node is a cross-community bridge._
- **Why does `ClinicaVisionModel` connect `Community 4` to `Community 1`, `Community 2`, `Community 3`, `Community 5`?**
  _High betweenness centrality (0.257) - this node is a cross-community bridge._
- **Why does `ClinicaLENSPipeline` connect `Community 2` to `Community 0`, `Community 1`, `Community 3`, `Community 4`, `Community 5`?**
  _High betweenness centrality (0.220) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `MedicalRAG` (e.g. with `ClinicaLENSPipeline` and `Unified Upgraded Pipeline for Clinica-LENS.     Orchestrates CheXNet Vision, Sa`) actually correct?**
  _`MedicalRAG` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `ClinicaVisionModel` (e.g. with `ClinicaLENSPipeline` and `Unified Upgraded Pipeline for Clinica-LENS.     Orchestrates CheXNet Vision, Sa`) actually correct?**
  _`ClinicaVisionModel` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `ClinicaFusionModel` (e.g. with `ClinicaLENSPipeline` and `Unified Upgraded Pipeline for Clinica-LENS.     Orchestrates CheXNet Vision, Sa`) actually correct?**
  _`ClinicaFusionModel` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `ClinicaLENSPipeline` (e.g. with `ClinicaVisionModel` and `ClinicaFusionModel`) actually correct?**
  _`ClinicaLENSPipeline` has 5 INFERRED edges - model-reasoned connections that need verification._