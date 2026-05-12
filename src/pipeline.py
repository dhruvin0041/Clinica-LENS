import torch
import torchvision.transforms as transforms
from PIL import Image
from src.models import ClinicaVisionModel, ClinicaFusionModel
from src.rag_pipeline import MedicalRAG
from src.xai import get_grad_cam

class ClinicaLENSPipeline:
    """
    Unified Pipeline for Clinica-LENS.
    Orchestrates Vision, RAG, and Fusion components.
    """
    def __init__(self, vision_model_path=None, fusion_model_path=None):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Initialize sub-models
        self.vision_model = ClinicaVisionModel().to(self.device)
        self.fusion_model = ClinicaFusionModel().to(self.device)
        self.rag_engine = MedicalRAG()
        
        # Load weights if provided (placeholders for now)
        if vision_model_path:
            self.vision_model.load_state_dict(torch.load(vision_model_path, map_location=self.device))
        if fusion_model_path:
            self.fusion_model.load_state_dict(torch.load(fusion_model_path, map_location=self.device))
            
        self.vision_model.eval()
        self.fusion_model.eval()
        
        # Standard preprocessing for ResNet50
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def predict(self, image_path, text_query):
        """
        Runs the multimodal prediction pipeline.
        """
        # 1. Process Image
        image = Image.open(image_path).convert('RGB')
        img_tensor = self.transform(image).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            vision_emb = self.vision_model(img_tensor)
        
        # 2. Get RAG Explanation and Text Embedding
        # Note: We use the RAG engine to get clinical context
        rag_output = self.rag_engine.explain_diagnosis(text_query)
        
        # Get the embedding of the query for the fusion layer
        # We use the same embedding model used in the RAG pipeline
        text_emb_list = self.rag_engine.embeddings.embed_query(text_query)
        text_emb = torch.tensor(text_emb_list).unsqueeze(0).to(self.device)
        
        # 3. Multimodal Fusion
        with torch.no_grad():
            logits = self.fusion_model(vision_emb, text_emb)
            probs = torch.softmax(logits, dim=1)
            prediction = torch.argmax(probs, dim=1).item()
            
        # 4. Generate XAI (Grad-CAM)
        # We target the last convolutional layer
        target_layer = self.vision_model.feature_extractor[-2]
        heatmap = get_grad_cam(self.vision_model, img_tensor, target_layer)
        
        return {
            "prediction": prediction,
            "probabilities": probs.squeeze().tolist(),
            "rag_explanation": rag_output["explanation"] if isinstance(rag_output, dict) else rag_output,
            "rag_sources": rag_output.get("sources", []) if isinstance(rag_output, dict) else [],
            "heatmap": heatmap
        }

if __name__ == "__main__":
    # Test with dummy inputs (Note: will fail if no PDFs or LLM not setup)
    # pipeline = ClinicaLENSPipeline()
    # print("Pipeline initialized.")
    pass
