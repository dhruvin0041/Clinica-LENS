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

    def predict(self, image_path, text_query, prior_image_path=None, window_center=None, window_width=None, mc_samples=10):
        """
        Runs the multimodal prediction pipeline with Temporal analysis and Counterfactuals.
        """
        # 1. Process Current Image
        image = self.load_and_window_image(image_path, window_center, window_width)
        img_tensor = self.transform(image).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            vision_features = self.vision_model(img_tensor, return_spatial=True)
            vision_emb = self.vision_model(img_tensor)
        
        # Phase 1: Longitudinal Analysis
        progression_score = 0.0
        if prior_image_path:
            prior_image = self.load_and_window_image(prior_image_path, window_center, window_width)
            prior_tensor = self.transform(prior_image).unsqueeze(0).to(self.device)
            with torch.no_grad():
                prior_emb = self.vision_model(prior_tensor)
                progression_score = self.temporal_model(vision_emb, prior_emb).item()
        
        # 2. RAG & Text Embedding (Phase 3: Structured Report)
        rag_output = self.rag_engine.explain_diagnosis(text_query)
        text_emb_list = self.rag_engine.embeddings.embed_query(text_query)
        text_emb = torch.tensor(text_emb_list).unsqueeze(0).to(self.device)
        
        # 3. MC Dropout for Uncertainty Estimation
        def enable_dropout(m):
            if type(m) == torch.nn.Dropout:
                m.train()
        
        self.fusion_model.eval()
        self.fusion_model.apply(enable_dropout)
        
        all_probs = []
        with torch.no_grad():
            for _ in range(mc_samples):
                logits = self.fusion_model(vision_features, text_emb)
                probs = torch.softmax(logits, dim=1)
                all_probs.append(probs)
        
        all_probs = torch.stack(all_probs)
        mean_probs = all_probs.mean(dim=0).squeeze()
        std_probs = all_probs.std(dim=0).squeeze()
        
        prediction = torch.argmax(mean_probs).item()
        uncertainty = std_probs[prediction].item()
            
        # 4. XAI (Grad-CAM)
        target_layer = self.vision_model.feature_extractor[-2]
        heatmap = get_grad_cam(self.vision_model, img_tensor, target_layer)
        
        # Phase 2: Counterfactual Explanation ("What-If")
        counterfactual_tensor = generate_counterfactual(self.vision_model, img_tensor, heatmap)
        with torch.no_grad():
            cf_vision_features = self.vision_model(counterfactual_tensor, return_spatial=True)
            cf_logits = self.fusion_model(cf_vision_features, text_emb)
            cf_probs = torch.softmax(cf_logits, dim=1).squeeze()
            prob_shift = mean_probs[prediction].item() - cf_probs[prediction].item()
        
        return {
            "prediction": prediction,
            "mean_probability": mean_probs[prediction].item(),
            "uncertainty": uncertainty,
            "progression_score": progression_score, # Phase 1
            "prob_shift": prob_shift, # Phase 2
            "findings": rag_output.get("findings", ""), # Phase 3
            "impression": rag_output.get("impression", ""), # Phase 3
            "rag_status": rag_output.get("status", "Unknown"),
            "rag_sources": rag_output.get("sources", []),
            "heatmap": heatmap
        }

    def chat(self, user_query):
        """Phase 4: Conversational VQA."""
        return self.rag_engine.chat_vqa(user_query)
