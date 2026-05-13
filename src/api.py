from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Any
import base64
from src.worker import predict_task
from celery.result import AsyncResult

app = FastAPI(title="Clinica-LENS API", description="Enterprise API for Multimodal Clinical Diagnostics")

class JobResponse(BaseModel):
    job_id: str
    status: str

class DiagnosisResponse(BaseModel):
    prediction: int
    mean_probability: float
    uncertainty: float
    prediction_set: List[int]
    progression_score: float
    prob_shift: float
    findings: str
    impression: str
    rag_status: str
    rag_sources: List[str]
    heatmap_b64: Optional[str] = None

@app.post("/predict", response_model=JobResponse)
async def predict(
    image: UploadFile = File(...),
    clinical_notes: str = Form(...),
    prior_image: Optional[UploadFile] = File(None),
    window_center: Optional[int] = Form(None),
    window_width: Optional[int] = Form(None)
):
    # Convert files to base64 for Celery transport
    image_content = await image.read()
    image_b64 = base64.b64encode(image_content).decode()
    
    prior_b64 = None
    if prior_image:
        prior_content = await prior_image.read()
        prior_b64 = base64.b64encode(prior_content).decode()
    
    # Dispatch task
    task = predict_task.delay(
        image_b64, 
        clinical_notes, 
        prior_image_data_b64=prior_b64,
        window_center=window_center,
        window_width=window_width
    )
    
    return {"job_id": task.id, "status": "PENDING"}

@app.get("/status/{job_id}")
async def get_status(job_id: str):
    task_result = AsyncResult(job_id)
    if task_result.status == 'PENDING':
        return {"job_id": job_id, "status": "PENDING"}
    elif task_result.status == 'SUCCESS':
        return {"job_id": job_id, "status": "SUCCESS", "result": task_result.result}
    elif task_result.status == 'FAILURE':
        return {"job_id": job_id, "status": "FAILURE", "error": str(task_result.info)}
    return {"job_id": job_id, "status": task_result.status}

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
