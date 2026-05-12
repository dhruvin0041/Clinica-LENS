import torch
import torch.nn as nn
from torchvision import models

class ClinicaVisionModel(nn.Module):
    """
    Encoder for Medical Images (X-rays).
    Uses a pre-trained ResNet/ViT and extracts feature embeddings.
    """
    def __init__(self, model_name='resnet50', embedding_dim=512):
        super(ClinicaVisionModel, self).__init__()
        if model_name == 'resnet50':
            self.backbone = models.resnet50(pretrained=True)
            # Remove the final classification layer to get embeddings
            self.feature_extractor = nn.Sequential(*list(self.backbone.children())[:-1])
            self.fc = nn.Linear(self.backbone.fc.in_features, embedding_dim)
        
    def forward(self, x):
        features = self.feature_extractor(x)
        features = torch.flatten(features, 1)
        embedding = self.fc(features)
        return embedding

class ClinicaFusionModel(nn.Module):
    """
    The Multimodal Fusion Layer.
    Combines Vision embeddings and Text embeddings to predict diagnosis.
    """
    def __init__(self, vision_dim=512, text_dim=768, hidden_dim=256, num_classes=2):
        super(ClinicaFusionModel, self).__init__()
        self.fusion_layer = nn.Sequential(
            nn.Linear(vision_dim + text_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim, num_classes)
        )
        
    def forward(self, vision_emb, text_emb):
        # Concatenate Vision and Text embeddings
        combined = torch.cat((vision_emb, text_emb), dim=1)
        logits = self.fusion_layer(combined)
        return logits

if __name__ == "__main__":
    # Test initialization
    v_model = ClinicaVisionModel()
    f_model = ClinicaFusionModel()
    print("Clinica-LENS Fusion Model Initialized successfully.")
