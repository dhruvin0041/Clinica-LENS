import pytest
import torch
import os
import sys
from unittest.mock import MagicMock, patch

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.models import ClinicaVisionModel, ClinicaFusionModel, ClinicaTemporalModel
from src.pipeline import ClinicaLENSPipeline
from src.rag_pipeline import MedicalRAG

def test_vision_model_forward():
    model = ClinicaVisionModel(embedding_dim=512)
    dummy_input = torch.randn(1, 3, 224, 224)
    output = model(dummy_input)
    assert output.shape == (1, 512)

def test_fusion_model_forward():
    model = ClinicaFusionModel(vision_channels=1024, text_dim=768, embed_dim=512)
    dummy_vision = torch.randn(1, 1024, 7, 7)
    dummy_text = torch.randn(1, 768)
    output = model(dummy_vision, dummy_text)
    assert output.shape == (1, 2) # num_classes=2

def test_temporal_model_forward():
    model = ClinicaTemporalModel(vision_dim=512)
    current_emb = torch.randn(1, 512)
    prior_emb = torch.randn(1, 512)
    output = model(current_emb, prior_emb)
    assert output.shape == (1, 1)
    assert -1 <= output.item() <= 1

@patch('src.rag_pipeline.HuggingFaceEmbeddings')
def test_rag_initialization(mock_embeddings):
    # Mock embeddings to avoid loading large models
    mock_embeddings.return_value = MagicMock()
    rag = MedicalRAG()
    assert rag is not None
    assert rag.embeddings is not None

@patch('src.pipeline.ClinicaVisionModel')
@patch('src.pipeline.ClinicaFusionModel')
@patch('src.pipeline.ClinicaTemporalModel')
@patch('src.pipeline.MedicalRAG')
def test_pipeline_initialization(mock_rag, mock_temp, mock_fusion, mock_vision):
    pipeline = ClinicaLENSPipeline()
    assert pipeline.vision_model is not None
    assert pipeline.fusion_model is not None
    assert pipeline.temporal_model is not None
    assert pipeline.rag_engine is not None
