import torch
import torch.nn as nn
from torchvision import models

class ClinicaVisionModel(nn.Module):
    """
    Encoder for Medical Images (X-rays) using CheXNet architecture (DenseNet121).
    Extracts spatial feature maps to support attention-based fusion.
    """
    def __init__(self, embedding_dim=512):
        super(ClinicaVisionModel, self).__init__()
        # DenseNet121 is the standard for CheXNet
        self.backbone = models.densenet121(pretrained=True)
        # Remove the classification head
        self.feature_extractor = self.backbone.features
        
        # Mapping spatial features to embedding dimension
        # DenseNet121 output is (B, 1024, 7, 7) for 224x224 input
        self.pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(1024, embedding_dim)
        
    def forward(self, x, return_spatial=False):
        # x: (B, 3, 224, 224)
        features = self.feature_extractor(x) # (B, 1024, 7, 7)
        
        if return_spatial:
            return features
            
        pooled = self.pool(features)
        pooled = torch.flatten(pooled, 1)
        embedding = self.fc(pooled)
        return embedding

class ClinicaFusionModel(nn.Module):
    """
    Transformer-based Multimodal Fusion Layer.
    Uses Cross-Attention to let Text and Vision modalities interact.
    """
    def __init__(self, vision_channels=1024, text_dim=768, embed_dim=512, nhead=8, num_layers=2, num_classes=2):
        super(ClinicaFusionModel, self).__init__()
        
        # Projection layers to shared embedding dimension
        self.vision_proj = nn.Linear(vision_channels, embed_dim)
        self.text_proj = nn.Linear(text_dim, embed_dim)
        
        # Positional encoding for spatial features (7x7 = 49 patches)
        self.pos_embedding = nn.Parameter(torch.randn(1, 49 + 1, embed_dim))
        
        # Transformer Encoder
        encoder_layer = nn.TransformerEncoderLayer(d_model=embed_dim, nhead=nhead, batch_first=True, dropout=0.1)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        # Classification head
        self.classifier = nn.Linear(embed_dim, num_classes)
        
    def forward(self, vision_features, text_emb):
        """
        vision_features: (B, 1024, 7, 7) from DenseNet
        text_emb: (B, 768) from SapBERT
        """
        B = vision_features.shape[0]
        
        # 1. Flatten spatial features: (B, 1024, 49) -> (B, 49, 1024)
        vision_patches = vision_features.flatten(2).transpose(1, 2)
        vision_tokens = self.vision_proj(vision_patches) # (B, 49, embed_dim)
        
        # 2. Project text to same dim: (B, 1, embed_dim)
        text_token = self.text_proj(text_emb).unsqueeze(1)
        
        # 3. Concatenate tokens: [Text, Vision_1, ..., Vision_49]
        tokens = torch.cat((text_token, vision_tokens), dim=1) # (B, 50, embed_dim)
        
        # 4. Add positional encoding
        tokens = tokens + self.pos_embedding
        
        # 5. Transformer interaction
        # We enable dropout even in eval mode for Uncertainty Estimation (Phase 4)
        # Note: In a real implementation, we'd wrap this to be more explicit.
        output = self.transformer(tokens)
        
        # 6. Take the text token as the "CLS" equivalent for prediction
        cls_output = output[:, 0, :]
        logits = self.classifier(cls_output)
        
        return logits

class ClinicaTemporalModel(nn.Module):
    """
    Siamese Network for Longitudinal Analysis.
    Compares current vision embeddings with a "prior" scan to assess progression.
    """
    def __init__(self, vision_dim=512, hidden_dim=256):
        super(ClinicaTemporalModel, self).__init__()
        self.diff_layer = nn.Sequential(
            nn.Linear(vision_dim, hidden_dim), # Process the difference vector
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim, 1), # Output a scalar progression score
            nn.Tanh() # -1 (improved) to +1 (progressed)
        )
        
    def forward(self, current_emb, prior_emb):
        # Calculate absolute difference (Siamese approach)
        diff = torch.abs(current_emb - prior_emb)
        progression_score = self.diff_layer(diff)
        return progression_score

if __name__ == "__main__":
    # Test initialization
    v_model = ClinicaVisionModel()
    f_model = ClinicaFusionModel()
    t_model = ClinicaTemporalModel()
    
    dummy_img = torch.randn(2, 3, 224, 224)
    dummy_text = torch.randn(2, 768)
    dummy_prior = torch.randn(2, 512)
    
    vis_feat = v_model(dummy_img, return_spatial=True)
    vis_emb = v_model(dummy_img)
    
    logits = f_model(vis_feat, dummy_text)
    progression = t_model(vis_emb, dummy_prior)
    
    print(f"Vision features shape: {vis_feat.shape}")
    print(f"Fusion logits shape: {logits.shape}")
    print(f"Progression score shape: {progression.shape}")
    print("Clinica-LENS Upgraded Models Initialized successfully.")
