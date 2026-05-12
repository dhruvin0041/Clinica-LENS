from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Optional
import os
import shutil
from src.pipeline import ClinicaLENSPipeline

app = FastAPI(title="Clinica-LENS API", description="Production API for Multimodal Clinical Diagnostics")

# Initialize pipeline (lazy load models in production)
pipeline = ClinicaLENSPipeline()

class DiagnosisResponse(BaseModel):
    prediction: int
    mean_probability: float
    uncertainty: float
    progression_score: float
    prob_shift: float
    findings: str
    impression: str
    rag_status: str
    rag_sources: List[str]

@app.post("/predict", response_model=DiagnosisResponse)
async def predict(
    image: UploadFile = File(...),
    clinical_notes: str = Form(...),
    prior_image: Optional[UploadFile] = File(None),
    window_center: Optional[int] = Form(None),
    window_width: Optional[int] = Form(None)
):
    # Save uploaded files temporarily
    image_path = f"temp_{image.filename}"
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    prior_path = None
    if prior_image:
        prior_path = f"temp_prior_{prior_image.filename}"
        with open(prior_path, "wb") as buffer:
            shutil.copyfileobj(prior_image.file, buffer)
    
    # Load RAG if not ready
    pipeline.rag_engine.load_vector_db()
    if not pipeline.rag_engine.qa_chain:
        pipeline.rag_engine.setup_llm()
        
    results = pipeline.predict(
        image_path, 
        clinical_notes, 
        prior_image_path=prior_path,
        window_center=window_center,
        window_width=window_width
    )
    
    # Clean up (optional in prod, use tempfile)
    os.remove(image_path)
    if prior_path:
        os.remove(prior_path)
        
    # Heatmap is excluded from Pydantic model for now as it's a tensor/array
    # In a real API, we'd return a URL or base64
    results.pop("heatmap", None)
    
    return results

@app.get("/health")
def health():
    return {"status": "healthy", "device": str(pipeline.device)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
