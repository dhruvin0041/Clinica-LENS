import os
from celery import Celery
from src.pipeline import ClinicaLENSPipeline
import base64
from io import BytesIO
from PIL import Image

celery_app = Celery(
    "clinica_lens_worker",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
)

# Global pipeline instance in the worker to avoid reloading for every task
pipeline = None

def get_pipeline():
    global pipeline
    if pipeline is None:
        pipeline = ClinicaLENSPipeline()
        # Initialize RAG if needed
        pipeline.rag_engine.load_vector_db()
        if not pipeline.rag_engine.qa_chain:
            pipeline.rag_engine.setup_llm()
    return pipeline

@celery_app.task(name="tasks.predict_task")
def predict_task(image_path, clinical_notes, prior_image_path=None, window_center=None, window_width=None):
    pipe = get_pipeline()
    
    try:
        results = pipe.predict(
            image_path, 
            clinical_notes, 
            prior_image_path=prior_path,
            window_center=window_center,
            window_width=window_width
        )
        
        # Convert heatmap (numpy array) to base64 for transport
        heatmap = results.pop("heatmap", None)
        if heatmap is not None:
            # Assume heatmap is a numpy array that can be converted to image
            # In a real system, we'd use the overlay_heatmap logic or similar
            # For simplicity, we'll just send it as a base64 encoded PNG
            from src.xai import overlay_heatmap
            # We need the original image for the overlay
            img = pipe.load_and_window_image(image_path, window_center, window_width)
            img.save("/tmp/bg.png")
            combined_img = overlay_heatmap("/tmp/bg.png", heatmap)
            
            buffered = BytesIO()
            combined_img.save(buffered, format="PNG")
            results["heatmap_b64"] = base64.b64encode(buffered.getvalue()).decode()
            
        return results
    finally:
        # Cleanup
        if image_path and os.path.exists(image_path):
            os.remove(image_path)
        if prior_path and os.path.exists(prior_path):
            os.remove(prior_path)
        if os.path.exists("/tmp/bg.png"):
            os.remove("/tmp/bg.png")
