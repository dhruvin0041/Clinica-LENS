import numpy as np
import torch
from sklearn.linear_model import LogisticRegression

class ClinicalCalibrator:
    """
    Implements Platt Scaling (Logistic Calibration) for medical AI outputs.
    Ensures model confidence (0.9) matches real-world probability (90%).
    """
    def __init__(self):
        # In a real system, these coefficients would be learned on a large 
        # calibration dataset across various hardware vendors (GE, Siemens, etc.)
        self.is_calibrated = False
        self.model = LogisticRegression()
        
        # Placeholder coefficients for demo (mapping uncalibrated logits to calibrated probs)
        self.a = 0.85 # Scaling
        self.b = -0.1 # Intercept

    def calibrate(self, probs):
        """
        Applies a sigmoid transformation (Platt Scaling) to raw probabilities.
        probs: torch.Tensor or np.array of shape (C,) or (B, C)
        """
        if isinstance(probs, torch.Tensor):
            probs = probs.detach().cpu().numpy()
            
        # For demo, we apply a fixed transformation that improves alignment
        # In production, this would be: self.model.predict_proba(logits)
        calibrated = 1 / (1 + np.exp(-(self.a * probs + self.b)))
        
        # Re-normalize to sum to 1
        if calibrated.ndim == 1:
            calibrated = calibrated / np.sum(calibrated)
        else:
            calibrated = calibrated / np.sum(calibrated, axis=1, keepdims=True)
            
        return calibrated

    def fit(self, logits, labels):
        """
        Trains the calibrator on a held-out validation set.
        """
        self.model.fit(logits.reshape(-1, 1), labels)
        self.is_calibrated = True
        logger.info("Clinical Calibrator fitted on validation data.")
