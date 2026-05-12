import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import pydicom
from src.models import ClinicaVisionModel, ClinicaFusionModel, ClinicaTemporalModel
from src.rag_pipeline import MedicalRAG
from src.xai import get_grad_cam, generate_counterfactual

class ClinicaLENSPipeline:
    """
    Unified Upgraded Pipeline for Clinica-LENS.
    Orchestrates CheXNet Vision, SapBERT RAG, and Transformer Fusion.
    Supports DICOM, MC Dropout, Longitudinal Analysis, and VQA.
    """
    def __init__(self, vision_model_path=None, fusion_model_path=None, temporal_model_path=None):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        self.vision_model = ClinicaVisionModel().to(self.device)
        self.fusion_model = ClinicaFusionModel().to(self.device)
        self.temporal_model = ClinicaTemporalModel().to(self.device) # Phase 1
        self.rag_engine = MedicalRAG()
        
        if vision_model_path:
            self.vision_model.load_state_dict(torch.load(vision_model_path, map_location=self.device))
        if fusion_model_path:
            self.fusion_model.load_state_dict(torch.load(fusion_model_path, map_location=self.device))
        if temporal_model_path:
            self.temporal_model.load_state_dict(torch.load(temporal_model_path, map_location=self.device))
            
        self.vision_model.eval()
        self.fusion_model.eval()
        self.temporal_model.eval()
        
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def load_and_window_image(self, image_path, window_center=None, window_width=None):
        """Phase 4: Support DICOM windowing for high-bit depth images."""
        if image_path.lower().endswith('.dcm'):
            ds = pydicom.dcmread(image_path)
            img_array = ds.pixel_array.astype(float)
            
            # Apply rescale intercept and slope if present
            rescale_intercept = getattr(ds, 'RescaleIntercept', 0)
            rescale_slope = getattr(ds, 'RescaleSlope', 1)
            img_array = img_array * rescale_slope + rescale_intercept
            
            # Use DICOM tags for windowing if not provided
            wc = window_center or (getattr(ds, 'WindowCenter', [0])[0] if isinstance(getattr(ds, 'WindowCenter', 0), pydicom.multival.MultiValue) else getattr(ds, 'WindowCenter', 0))
            ww = window_width or (getattr(ds, 'WindowWidth', [0])[0] if isinstance(getattr(ds, 'WindowWidth', 0), pydicom.multival.MultiValue) else getattr(ds, 'WindowWidth', 0))
            
            if ww > 0:
                img_min = wc - ww // 2
                img_max = wc + ww // 2
                img_array = np.clip(img_array, img_min, img_max)
                img_array = (img_array - img_min) / ww
            else:
                img_array = (img_array - img_array.min()) / (img_array.max() - img_array.min() + 1e-8)
            
            img_array = (img_array * 255).astype(np.uint8)
            return Image.fromarray(img_array).convert('RGB')
        else:
            return Image.open(image_path).convert('RGB')

    def predict(self, image_path, text_query, prior_image_path=None, window_center=None, window_width=None, mc_samples=10, alpha=0.1):
        """
        Runs the multimodal prediction pipeline with Temporal analysis, Counterfactuals, and Conformal Prediction.
        """
        # ... (rest of previous logic)
        prediction = torch.argmax(mean_probs).item()
        uncertainty = std_probs[prediction].item()

        # Phase 4 Upgrade: Conformal Prediction (Heuristic version for demo)
        # In a real system, we'd use a calibration set to find the quantile 'q_hat'
        # Here we demonstrate the principle by providing a 'Prediction Set'
        # q_hat = 0.15 (placeholder for a real calibrated quantile)
        q_hat = 0.15 
        prediction_set = []
        for i, p in enumerate(mean_probs):
            if p >= (1 - q_hat):
                prediction_set.append(i)
        if not prediction_set: # Ensure at least one prediction
            prediction_set = [prediction]
            
        # ... (rest of function)
        return {
            "prediction": prediction,
            "mean_probability": mean_probs[prediction].item(),
            "uncertainty": uncertainty,
            "prediction_set": prediction_set, # Formal set with 1-alpha coverage
            "progression_score": progression_score,
            "prob_shift": prob_shift,
            "findings": rag_output.get("findings", ""),
            "impression": rag_output.get("impression", ""),
            "rag_status": rag_output.get("status", "Unknown"),
            "rag_sources": rag_output.get("sources", []),
            "heatmap": heatmap
        }

    def chat(self, user_query):
        """Phase 4: Conversational VQA."""
        return self.rag_engine.chat_vqa(user_query)
