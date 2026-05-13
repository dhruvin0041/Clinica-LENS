# Graph Report - Clinica-LENS  (2026-05-13)

## Corpus Check
- 9 files · ~19,848 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 72 nodes · 97 edges · 12 communities detected
- Extraction: 59% EXTRACTED · 41% INFERRED · 0% AMBIGUOUS · INFERRED: 40 edges (avg confidence: 0.62)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]

## God Nodes (most connected - your core abstractions)
1. `ClinicaLENSPipeline` - 16 edges
2. `MedicalRAG` - 16 edges
3. `ClinicaVisionModel` - 14 edges
4. `ClinicaFusionModel` - 11 edges
5. `ClinicaTemporalModel` - 11 edges
6. `Unified Upgraded Pipeline for Clinica-LENS.     Orchestrates CheXNet Vision, Sa` - 5 edges
7. `Phase 4: Support DICOM windowing for high-bit depth images.` - 5 edges
8. `Runs the multimodal prediction pipeline with Temporal analysis, Counterfactuals,` - 5 edges
9. `Phase 4: Conversational VQA.` - 5 edges
10. `DiagnosisResponse` - 3 edges

## Surprising Connections (you probably didn't know these)
- `ClinicaLENSPipeline` --processed_by--> `Current X-ray Scan`  [INFERRED]
  src\pipeline.py → temp_image.png
- `ClinicaLENSPipeline` --sample_for--> `Bacterial Pneumonia Sample`  [INFERRED]
  src\pipeline.py → data/sample_images/person1000_bacteria_2931.jpeg
- `ClinicaLENSPipeline` --sample_for--> `Viral Pneumonia Sample`  [INFERRED]
  src\pipeline.py → data/sample_images/person1009_virus_1694.jpeg
- `ClinicaVisionModel` --calls--> `test_vision_model_forward()`  [INFERRED]
  src\models.py → tests\test_core.py
- `ClinicaFusionModel` --calls--> `test_fusion_model_forward()`  [INFERRED]
  src\models.py → tests\test_core.py

## Hyperedges (group relationships)
- **Multimodal Diagnostic Stack** — models_clinicavisionmodel, models_clinicafusionmodel, rag_pipeline_medicalrag [INFERRED 0.90]

## Communities

### Community 0 - "Community 0"
Cohesion: 0.18
Nodes (6): ClinicaFusionModel, ClinicaTemporalModel, Transformer-based Multimodal Fusion Layer.     Uses Cross-Attention to let Text, vision_features: (B, 1024, 7, 7) from DenseNet         text_emb: (B, 768) from, Siamese Network for Longitudinal Analysis.     Compares current vision embeddin, Phase 4: Support DICOM windowing for high-bit depth images.

### Community 1 - "Community 1"
Cohesion: 0.16
Nodes (7): Phase 4: Conversational VQA., MedicalRAG, Phase 2: NLI-based Fact Checking., Generates a verified structured report., Upgraded Retrieval-Augmented Generation pipeline for Clinica-LENS.     Uses Sap, Phase 4: Conversational Visual QA loop., Loads PDFs, splits them, and creates Hybrid Search indexes.

### Community 2 - "Community 2"
Cohesion: 0.2
Nodes (7): load_pipeline(), Bacterial Pneumonia Sample, Viral Pneumonia Sample, ClinicaLENSPipeline, Unified Upgraded Pipeline for Clinica-LENS.     Orchestrates CheXNet Vision, Sa, Runs the multimodal prediction pipeline with Temporal analysis, Counterfactuals,, Current X-ray Scan

### Community 3 - "Community 3"
Cohesion: 0.24
Nodes (8): ClinicaVisionModel, Encoder for Medical Images (X-rays) using CheXNet architecture (DenseNet121)., generate_counterfactual(), get_grad_cam(), overlay_heatmap(), Overlays a heatmap onto an image., Phase 3 Upgrade: Generates a counterfactual image using OpenCV Inpainting., Generates Grad-CAM heatmaps for a given model and input image.          Args:

### Community 4 - "Community 4"
Cohesion: 0.22
Nodes (5): DiagnosisResponse, predict(), BaseModel, Initializes a local LLM and the RAG chain., Loads existing FAISS and reconstructs BM25 index from stored docs.

### Community 5 - "Community 5"
Cohesion: 0.33
Nodes (5): test_fusion_model_forward(), test_pipeline_initialization(), test_rag_initialization(), test_temporal_model_forward(), test_vision_model_forward()

### Community 6 - "Community 6"
Cohesion: 1.0
Nodes (2): Agent Workflow Instructions, Project Instructions

### Community 9 - "Community 9"
Cohesion: 1.0
Nodes (1): Project Documentation

### Community 10 - "Community 10"
Cohesion: 1.0
Nodes (1): Project Dependencies

### Community 11 - "Community 11"
Cohesion: 1.0
Nodes (1): SapBERT Medical Embeddings

### Community 12 - "Community 12"
Cohesion: 1.0
Nodes (1): BGE Cross-Encoder Re-ranker

### Community 13 - "Community 13"
Cohesion: 1.0
Nodes (1): NLI Fact-Checking Guardrails

## Knowledge Gaps
- **21 isolated node(s):** `Encoder for Medical Images (X-rays) using CheXNet architecture (DenseNet121).`, `Transformer-based Multimodal Fusion Layer.     Uses Cross-Attention to let Text`, `vision_features: (B, 1024, 7, 7) from DenseNet         text_emb: (B, 768) from`, `Siamese Network for Longitudinal Analysis.     Compares current vision embeddin`, `Upgraded Retrieval-Augmented Generation pipeline for Clinica-LENS.     Uses Sap` (+16 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 6`** (2 nodes): `Agent Workflow Instructions`, `Project Instructions`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 9`** (1 nodes): `Project Documentation`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 10`** (1 nodes): `Project Dependencies`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 11`** (1 nodes): `SapBERT Medical Embeddings`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 12`** (1 nodes): `BGE Cross-Encoder Re-ranker`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 13`** (1 nodes): `NLI Fact-Checking Guardrails`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `MedicalRAG` connect `Community 1` to `Community 0`, `Community 2`, `Community 4`, `Community 5`?**
  _High betweenness centrality (0.339) - this node is a cross-community bridge._
- **Why does `ClinicaLENSPipeline` connect `Community 2` to `Community 0`, `Community 1`, `Community 3`, `Community 4`, `Community 5`?**
  _High betweenness centrality (0.297) - this node is a cross-community bridge._
- **Why does `ClinicaVisionModel` connect `Community 3` to `Community 0`, `Community 1`, `Community 2`, `Community 5`?**
  _High betweenness centrality (0.246) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `ClinicaLENSPipeline` (e.g. with `DiagnosisResponse` and `ClinicaVisionModel`) actually correct?**
  _`ClinicaLENSPipeline` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `MedicalRAG` (e.g. with `ClinicaLENSPipeline` and `Unified Upgraded Pipeline for Clinica-LENS.     Orchestrates CheXNet Vision, Sa`) actually correct?**
  _`MedicalRAG` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `ClinicaVisionModel` (e.g. with `ClinicaLENSPipeline` and `Unified Upgraded Pipeline for Clinica-LENS.     Orchestrates CheXNet Vision, Sa`) actually correct?**
  _`ClinicaVisionModel` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `ClinicaFusionModel` (e.g. with `ClinicaLENSPipeline` and `Unified Upgraded Pipeline for Clinica-LENS.     Orchestrates CheXNet Vision, Sa`) actually correct?**
  _`ClinicaFusionModel` has 7 INFERRED edges - model-reasoned connections that need verification._