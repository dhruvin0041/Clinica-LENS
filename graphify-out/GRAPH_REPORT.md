# Graph Report - .  (2026-05-12)

## Corpus Check
- Corpus is ~17,496 words - fits in a single context window. You may not need a graph.

## Summary
- 53 nodes · 66 edges · 11 communities detected
- Extraction: 61% EXTRACTED · 39% INFERRED · 0% AMBIGUOUS · INFERRED: 26 edges (avg confidence: 0.66)
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
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]

## God Nodes (most connected - your core abstractions)
1. `MedicalRAG` - 14 edges
2. `ClinicaVisionModel` - 11 edges
3. `ClinicaFusionModel` - 11 edges
4. `ClinicaLENSPipeline` - 11 edges
5. `get_grad_cam` - 7 edges
6. `Unified Upgraded Pipeline for Clinica-LENS.     Orchestrates CheXNet Vision, Sa` - 5 edges
7. `Phase 4: Support DICOM windowing for high-bit depth images.` - 5 edges
8. `Runs the multimodal prediction pipeline with MC Dropout for Uncertainty.` - 5 edges
9. `load_pipeline()` - 2 edges
10. `Streamlit Dashboard` - 2 edges

## Surprising Connections (you probably didn't know these)
- `Multimodal Fusion Concept` --semantically_similar_to--> `ClinicaFusionModel`  [INFERRED] [semantically similar]
  README.md → C:\DATA SCIENCE\Project\Clinica-LENS\src\models.py
- `RAG Concept` --semantically_similar_to--> `MedicalRAG`  [INFERRED] [semantically similar]
  README.md → C:\DATA SCIENCE\Project\Clinica-LENS\src\rag_pipeline.py
- `Explainable AI (XAI) Concept` --semantically_similar_to--> `get_grad_cam`  [INFERRED] [semantically similar]
  README.md → src/xai.py
- `Radiographic Findings of CAP` --conceptually_related_to--> `ClinicaVisionModel`  [INFERRED]
  data/medical_literature/cap_summary.txt → C:\DATA SCIENCE\Project\Clinica-LENS\src\models.py
- `load_pipeline()` --calls--> `ClinicaLENSPipeline`  [INFERRED]
  C:\DATA SCIENCE\Project\Clinica-LENS\app\app.py → C:\DATA SCIENCE\Project\Clinica-LENS\src\pipeline.py

## Hyperedges (group relationships)
- **Clinica-LENS Core Architecture** — pipeline_clinicalenspipeline, models_clinicavisionmodel, models_clinicafusionmodel, rag_pipeline_medicalrag, xai_get_grad_cam [INFERRED 0.90]

## Communities

### Community 0 - "Community 0"
Cohesion: 0.25
Nodes (6): Community-Acquired Pneumonia (CAP), CURB-65 Severity Assessment, Radiographic Findings of CAP, ClinicaVisionModel, Uses pre-trained ResNet/ViT for feature embeddings, Encoder for Medical Images (X-rays) using CheXNet architecture (DenseNet121).

### Community 1 - "Community 1"
Cohesion: 0.25
Nodes (5): ClinicaFusionModel, Combines Vision and Text embeddings to predict diagnosis, Transformer-based Multimodal Fusion Layer.     Uses Cross-Attention to let Text, vision_features: (B, 1024, 7, 7) from DenseNet         text_emb: (B, 768) from, Multimodal Fusion Concept

### Community 2 - "Community 2"
Cohesion: 0.32
Nodes (6): Unified Upgraded Pipeline for Clinica-LENS.     Orchestrates CheXNet Vision, Sa, Phase 4: Support DICOM windowing for high-bit depth images., Runs the multimodal prediction pipeline with MC Dropout for Uncertainty., Explainable AI (XAI) Concept, get_grad_cam, Attribute to sum of embedding to see global features

### Community 3 - "Community 3"
Cohesion: 0.29
Nodes (4): load_pipeline(), Streamlit Dashboard, ClinicaLENSPipeline, overlay_heatmap

### Community 4 - "Community 4"
Cohesion: 0.4
Nodes (3): MedicalRAG, Upgraded Retrieval-Augmented Generation pipeline for Clinica-LENS.     Uses Sap, RAG Concept

### Community 5 - "Community 5"
Cohesion: 0.5
Nodes (2): Phase 5: Self-Correction Loop / Hallucination Guardrail., Generates a verified explanation.

### Community 6 - "Community 6"
Cohesion: 1.0
Nodes (1): Initializes a local LLM and the RAG chain.

### Community 7 - "Community 7"
Cohesion: 1.0
Nodes (1): Loads PDFs, splits them, and creates Hybrid Search indexes.

### Community 8 - "Community 8"
Cohesion: 1.0
Nodes (1): Loads existing FAISS and reconstructs BM25 index from stored docs.

### Community 14 - "Community 14"
Cohesion: 1.0
Nodes (1): Chest X-ray: Bacterial Pneumonia

### Community 15 - "Community 15"
Cohesion: 1.0
Nodes (1): Chest X-ray: Viral Pneumonia

## Knowledge Gaps
- **19 isolated node(s):** `Encoder for Medical Images (X-rays) using CheXNet architecture (DenseNet121).`, `Transformer-based Multimodal Fusion Layer.     Uses Cross-Attention to let Text`, `vision_features: (B, 1024, 7, 7) from DenseNet         text_emb: (B, 768) from`, `Upgraded Retrieval-Augmented Generation pipeline for Clinica-LENS.     Uses Sap`, `Loads PDFs, splits them, and creates Hybrid Search indexes.` (+14 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 5`** (4 nodes): `.explain_diagnosis()`, `.verify_explanation()`, `Phase 5: Self-Correction Loop / Hallucination Guardrail.`, `Generates a verified explanation.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 6`** (2 nodes): `.setup_llm()`, `Initializes a local LLM and the RAG chain.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 7`** (2 nodes): `.ingest_documents()`, `Loads PDFs, splits them, and creates Hybrid Search indexes.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 8`** (2 nodes): `.load_vector_db()`, `Loads existing FAISS and reconstructs BM25 index from stored docs.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 14`** (1 nodes): `Chest X-ray: Bacterial Pneumonia`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 15`** (1 nodes): `Chest X-ray: Viral Pneumonia`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `MedicalRAG` connect `Community 4` to `Community 2`, `Community 3`, `Community 5`, `Community 6`, `Community 7`, `Community 8`?**
  _High betweenness centrality (0.370) - this node is a cross-community bridge._
- **Why does `ClinicaLENSPipeline` connect `Community 3` to `Community 0`, `Community 1`, `Community 2`, `Community 4`?**
  _High betweenness centrality (0.242) - this node is a cross-community bridge._
- **Why does `ClinicaVisionModel` connect `Community 0` to `Community 1`, `Community 2`, `Community 3`?**
  _High betweenness centrality (0.223) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `MedicalRAG` (e.g. with `ClinicaLENSPipeline` and `Unified Upgraded Pipeline for Clinica-LENS.     Orchestrates CheXNet Vision, Sa`) actually correct?**
  _`MedicalRAG` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `ClinicaVisionModel` (e.g. with `ClinicaLENSPipeline` and `Unified Upgraded Pipeline for Clinica-LENS.     Orchestrates CheXNet Vision, Sa`) actually correct?**
  _`ClinicaVisionModel` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `ClinicaFusionModel` (e.g. with `ClinicaLENSPipeline` and `Unified Upgraded Pipeline for Clinica-LENS.     Orchestrates CheXNet Vision, Sa`) actually correct?**
  _`ClinicaFusionModel` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `ClinicaLENSPipeline` (e.g. with `ClinicaVisionModel` and `ClinicaFusionModel`) actually correct?**
  _`ClinicaLENSPipeline` has 5 INFERRED edges - model-reasoned connections that need verification._