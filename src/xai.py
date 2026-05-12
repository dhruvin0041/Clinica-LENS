import torch
import torch.nn.functional as F
import numpy as np
import matplotlib.pyplot as plt
from captum.attr import LayerGradCam
from PIL import Image

def get_grad_cam(model, input_tensor, target_layer):
    """
    Generates Grad-CAM heatmaps for a given model and input image.
    
    Args:
        model: The PyTorch model (ClinicaVisionModel).
        input_tensor: Preprocessed image tensor (1, 3, H, W).
        target_layer: The layer to compute Grad-CAM for (e.g., model.feature_extractor[-2]).
    """
    model.eval()
    lgc = LayerGradCam(model, target_layer)
    
    # For embeddings, we can compute attribution for each dimension or the sum.
    # Here, we'll attribute to the magnitude of the embedding.
    def model_forward(x):
        emb = model(x)
        return emb.norm(dim=1)
    
    # We redefine the lgc with a wrapper if needed, but LayerGradCam 
    # usually works on the model's forward output.
    # Since our vision model returns embeddings (batch, 512), 
    # let's attribute to the sum of the embedding to see what features it's looking at globally.
    
    # Create a wrapper that returns a scalar for attribution
    class ModelWrapper(torch.nn.Module):
        def __init__(self, original_model):
            super().__init__()
            self.original_model = original_model
        def forward(self, x):
            return self.original_model(x).sum(dim=1)

    wrapped_model = ModelWrapper(model)
    lgc_wrapped = LayerGradCam(wrapped_model, target_layer)
    
    attributions = lgc_wrapped.attribute(input_tensor)
    
    # Upsample the attribution to match input size
    upsampled_attr = LayerGradCam.interpolate(attributions, input_tensor.shape[2:])
    return upsampled_attr

def overlay_heatmap(img_path, heatmap, alpha=0.5, colormap=plt.cm.jet):
    """
    Overlays a heatmap onto an image.
    """
    img = Image.open(img_path).convert('RGB')
    img_np = np.array(img) / 255.0
    
    # Normalize heatmap
    heatmap = heatmap.squeeze().cpu().detach().numpy()
    heatmap = (heatmap - heatmap.min()) / (heatmap.max() - heatmap.min() + 1e-8)
    
    # Apply colormap
    heatmap_colored = colormap(heatmap)[:, :, :3]
    
    # Overlay
    combined = (1 - alpha) * img_np + alpha * heatmap_colored
    combined = np.clip(combined, 0, 1)
    
    return combined

import cv2

def generate_counterfactual(model, input_tensor, heatmap, threshold=0.6):
    """
    Phase 3 Upgrade: Generates a counterfactual image using OpenCV Inpainting.
    Instead of just blacking out regions, it fills them with surrounding 'normal' textures.
    """
    # 1. Prepare mask from heatmap
    heatmap_norm = (heatmap - heatmap.min()) / (heatmap.max() - heatmap.min() + 1e-8)
    mask = (heatmap_norm > threshold).float().squeeze().cpu().numpy()
    mask = (mask * 255).astype(np.uint8)
    
    # 2. Convert input_tensor back to image for CV2
    # Inverse normalize
    mean = torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1).to(input_tensor.device)
    std = torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1).to(input_tensor.device)
    unnorm_img = input_tensor * std + mean
    
    img_np = unnorm_img.squeeze().permute(1, 2, 0).cpu().detach().numpy()
    img_np = (np.clip(img_np, 0, 1) * 255).astype(np.uint8)
    
    # 3. Apply Inpainting
    # Resize mask if needed
    if mask.shape != img_np.shape[:2]:
        mask = cv2.resize(mask, (img_np.shape[1], img_np.shape[0]))
    
    inpainted = cv2.inpaint(img_np, mask, 3, cv2.INPAINT_TELEA)
    
    # 4. Convert back to tensor
    inpainted_tensor = torch.from_numpy(inpainted).permute(2, 0, 1).float() / 255.0
    inpainted_tensor = (inpainted_tensor - mean.squeeze().cpu()) / std.squeeze().cpu()
    
    return inpainted_tensor.unsqueeze(0).to(input_tensor.device)

if __name__ == "__main__":
    from src.models import ClinicaVisionModel
    import torchvision.transforms as transforms
    
    # Mock test
    model = ClinicaVisionModel()
    dummy_img = torch.randn(1, 3, 224, 224)
    # Target the last conv layer: layer4 in ResNet50
    # In ClinicaVisionModel, feature_extractor is Sequential(*list(backbone.children())[:-1])
    # ResNet children: conv1, bn1, relu, maxpool, layer1, layer2, layer3, layer4, avgpool, (fc removed)
    # feature_extractor has index -1 as avgpool, -2 as layer4
    target = model.feature_extractor[-2]
    
    attr = get_grad_cam(model, dummy_img, target)
    print(f"Grad-CAM attribution shape: {attr.shape}")
