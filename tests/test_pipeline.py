import pytest
import torch
import numpy as np
from unittest.mock import patch, MagicMock
from src.models import ClinicaVisionModel, ClinicaFusionModel, ClinicaTemporalModel
from src.pipeline import ClinicaLENSPipeline

def test_vision_model_return_spatial():
    model = ClinicaVisionModel()
    dummy_img = torch.randn(1, 3, 224, 224)
    out_spatial = model(dummy_img, return_spatial=True)
    assert out_spatial.shape == (1, 1024, 7, 7)

def test_temporal_model_forward():
    model = ClinicaTemporalModel()
    dummy_curr = torch.randn(1, 512)
    dummy_prior = torch.randn(1, 512)
    out = model(dummy_curr, dummy_prior)
    assert out.shape == (1, 1)

@patch("src.pipeline.MedicalRAG")
@patch("src.pipeline.ClinicalCalibrator")
def test_pipeline_predict_no_prior(mock_calibrator, mock_rag):
    # Mock Calibrator
    mock_calib_instance = MagicMock()
    mock_calib_instance.calibrate.return_value = np.array([0.1, 0.9])
    mock_calibrator.return_value = mock_calib_instance
    
    # Mock RAG
    mock_rag_instance = MagicMock()
    mock_rag_instance.generate_verified_report.return_value = {
        "findings": "Test findings",
        "impression": "Test impression",
        "status": "Verified",
        "sources": ["source1.pdf"]
    }
    mock_rag.return_value = mock_rag_instance
    
    pipeline = ClinicaLENSPipeline()
    
    # Patch vision and fusion to avoid heavy compute
    pipeline.vision_model = MagicMock()
    pipeline.vision_model.return_value = torch.randn(10, 512)
    
    pipeline.fusion_model = MagicMock()
    pipeline.fusion_model.return_value = torch.randn(10, 2)
    
    # Patch image loading
    pipeline.load_and_window_image = MagicMock()
    pipeline.load_and_window_image.return_value = MagicMock()
    
    pipeline.transform = MagicMock()
    pipeline.transform.return_value = torch.randn(3, 224, 224)
    
    # Patch XAI
    with patch("src.pipeline.get_grad_cam") as mock_cam, \
         patch("src.pipeline.generate_counterfactual") as mock_cf:
        mock_cam.return_value = torch.randn(1, 1, 224, 224)
        mock_cf.return_value = 0.05
        
        result = pipeline.predict(
            image_path="test.png",
            text_query="What is this?",
            mc_samples=10
        )
        
        assert "prediction" in result
        assert result["findings"] == "Test findings"
        assert result["rag_status"] == "Verified"

def test_pipeline_chat():
    pipeline = ClinicaLENSPipeline()
    pipeline.rag_engine.chat_vqa = MagicMock(return_value="Chat response")
    
    response = pipeline.chat("Tell me about the scan.")
    assert response == "Chat response"
