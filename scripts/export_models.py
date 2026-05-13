import torch
import os
from src.models import ClinicaVisionModel, ClinicaFusionModel, ClinicaTemporalModel

def export_to_torchscript():
    """
    Exports PyTorch models to TorchScript (.pt) for high-performance 
    serving via NVIDIA Triton or TorchServe.
    """
    os.makedirs("models/export", exist_ok=True)
    device = torch.device("cpu")
    
    print("Exporting ClinicaVisionModel...")
    vision = ClinicaVisionModel().to(device).eval()
    dummy_input = torch.randn(1, 3, 224, 224).to(device)
    traced_vision = torch.jit.trace(vision, dummy_input)
    traced_vision.save("models/export/vision_model.pt")
    
    print("Exporting ClinicaFusionModel...")
    fusion = ClinicaFusionModel().to(device).eval()
    dummy_vision_emb = torch.randn(1, 1024, 7, 7).to(device)
    dummy_text_emb = torch.randn(1, 768).to(device)
    traced_fusion = torch.jit.trace(fusion, (dummy_vision_emb, dummy_text_emb))
    traced_fusion.save("models/export/fusion_model.pt")
    
    print("Exporting ClinicaTemporalModel...")
    temporal = ClinicaTemporalModel().to(device).eval()
    dummy_curr = torch.randn(1, 1024).to(device)
    dummy_prior = torch.randn(1, 1024).to(device)
    traced_temporal = torch.jit.trace(temporal, (dummy_curr, dummy_prior))
    traced_temporal.save("models/export/temporal_model.pt")
    
    print("Models exported successfully to models/export/")

if __name__ == "__main__":
    export_to_torchscript()
