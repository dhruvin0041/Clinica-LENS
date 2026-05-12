# Graph Report - .  (2026-05-12)

## Corpus Check
- Corpus is ~11,382 words - fits in a single context window. You may not need a graph.

## Summary
- 50 nodes · 58 edges · 8 communities detected
- Extraction: 64% EXTRACTED · 36% INFERRED · 0% AMBIGUOUS · INFERRED: 21 edges (avg confidence: 0.7)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]

## God Nodes (most connected - your core abstractions)
1. `ClinicaVisionModel` - 12 edges
2. `MedicalRAG` - 12 edges
3. `ClinicaFusionModel` - 10 edges
4. `ClinicaLENSPipeline` - 9 edges
5. `get_grad_cam()` - 5 edges
6. `Unified Pipeline for Clinica-LENS.     Orchestrates Vision, RAG, and Fusion com` - 4 edges
7. `Runs the multimodal prediction pipeline.` - 4 edges
8. `overlay_heatmap()` - 3 edges
9. `load_pipeline()` - 2 edges
10. `Generates Grad-CAM heatmaps for a given model and input image.          Args:` - 2 edges

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
Cohesion: 0.18
Nodes (6): MedicalRAG, Retrieval-Augmented Generation pipeline for Clinica-LENS.     Reads medical lit, Loads PDFs, splits them, and creates a FAISS vector database., Loads an existing FAISS vector database., Initializes a local HuggingFace LLM for text generation., RAG Concept

### Community 1 - "Community 1"
Cohesion: 0.25
Nodes (4): ClinicaFusionModel, Combines Vision and Text embeddings to predict diagnosis, The Multimodal Fusion Layer.     Combines Vision embeddings and Text embeddings, Multimodal Fusion Concept

### Community 2 - "Community 2"
Cohesion: 0.25
Nodes (7): Streamlit Dashboard, Explainable AI (XAI) Concept, get_grad_cam(), Attribute to sum of embedding to see global features, overlay_heatmap(), Overlays a heatmap onto an image., Generates Grad-CAM heatmaps for a given model and input image.          Args:

### Community 3 - "Community 3"
Cohesion: 0.29
Nodes (6): Community-Acquired Pneumonia (CAP), CURB-65 Severity Assessment, Radiographic Findings of CAP, ClinicaVisionModel, Uses pre-trained ResNet/ViT for feature embeddings, Encoder for Medical Images (X-rays).     Uses a pre-trained ResNet/ViT and extr

### Community 4 - "Community 4"
Cohesion: 0.33
Nodes (3): load_pipeline(), ClinicaLENSPipeline, Unified Pipeline for Clinica-LENS.     Orchestrates Vision, RAG, and Fusion com

### Community 5 - "Community 5"
Cohesion: 0.5
Nodes (2): Runs the multimodal prediction pipeline., Generates an explanation based on the query and retrieved context.

### Community 10 - "Community 10"
Cohesion: 1.0
Nodes (1): Chest X-ray: Bacterial Pneumonia

### Community 11 - "Community 11"
Cohesion: 1.0
Nodes (1): Chest X-ray: Viral Pneumonia

## Knowledge Gaps
- **16 isolated node(s):** `Encoder for Medical Images (X-rays).     Uses a pre-trained ResNet/ViT and extr`, `The Multimodal Fusion Layer.     Combines Vision embeddings and Text embeddings`, `Retrieval-Augmented Generation pipeline for Clinica-LENS.     Reads medical lit`, `Loads PDFs, splits them, and creates a FAISS vector database.`, `Loads an existing FAISS vector database.` (+11 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 5`** (4 nodes): `.predict()`, `Runs the multimodal prediction pipeline.`, `.explain_diagnosis()`, `Generates an explanation based on the query and retrieved context.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 10`** (1 nodes): `Chest X-ray: Bacterial Pneumonia`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 11`** (1 nodes): `Chest X-ray: Viral Pneumonia`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `MedicalRAG` connect `Community 0` to `Community 4`, `Community 5`?**
  _High betweenness centrality (0.345) - this node is a cross-community bridge._
- **Why does `ClinicaVisionModel` connect `Community 3` to `Community 1`, `Community 2`, `Community 4`, `Community 5`?**
  _High betweenness centrality (0.295) - this node is a cross-community bridge._
- **Why does `ClinicaLENSPipeline` connect `Community 4` to `Community 0`, `Community 1`, `Community 2`, `Community 3`, `Community 5`?**
  _High betweenness centrality (0.246) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `ClinicaVisionModel` (e.g. with `ClinicaLENSPipeline` and `Unified Pipeline for Clinica-LENS.     Orchestrates Vision, RAG, and Fusion com`) actually correct?**
  _`ClinicaVisionModel` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `MedicalRAG` (e.g. with `ClinicaLENSPipeline` and `Unified Pipeline for Clinica-LENS.     Orchestrates Vision, RAG, and Fusion com`) actually correct?**
  _`MedicalRAG` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `ClinicaFusionModel` (e.g. with `ClinicaLENSPipeline` and `Unified Pipeline for Clinica-LENS.     Orchestrates Vision, RAG, and Fusion com`) actually correct?**
  _`ClinicaFusionModel` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `ClinicaLENSPipeline` (e.g. with `ClinicaVisionModel` and `ClinicaFusionModel`) actually correct?**
  _`ClinicaLENSPipeline` has 4 INFERRED edges - model-reasoned connections that need verification._