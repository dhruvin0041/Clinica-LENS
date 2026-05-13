from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional, Any
import base64
import time
import logging
from datetime import timedelta
from src.worker import predict_task
from src.auth import (
    Token, User, get_current_user, authenticate_user, 
    create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, fake_users_db, verify_password
)
from celery.result import AsyncResult

# Configure Logging
logging.basicConfig(
    filename="audit.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("Clinica-LENS-Audit")

app = FastAPI(title="Clinica-LENS API", description="Enterprise API for Multimodal Clinical Diagnostics")

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

# Metrics
REQUEST_COUNT = Counter("api_requests_total", "Total count of requests", ["method", "endpoint", "status"])
REQUEST_LATENCY = Histogram("api_request_latency_seconds", "Request latency", ["method", "endpoint"])

# Middleware for Audit Logging & Metrics
@app.middleware("http")
async def audit_log_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # Update Metrics
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path, status=response.status_code).inc()
    REQUEST_LATENCY.labels(method=request.method, endpoint=request.url.path).observe(process_time)
    
    logger.info(f"Method: {request.method} Path: {request.url.path} Status: {response.status_code} Duration: {process_time:.4f}s")
    return response

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

class FeedbackRequest(BaseModel):
    job_id: str
    rating: int # 1 to 5
    comments: Optional[str] = None
    radiologist_override: Optional[str] = None

@app.post("/feedback")
async def submit_feedback(feedback: FeedbackRequest, current_user: User = Depends(get_current_user)):
    """Human-in-the-Loop (HITL) feedback endpoint."""
    logger.info(f"User {current_user.username} submitted feedback for job {feedback.job_id}. Rating: {feedback.rating}")
    # In a real system, we'd save this to a database for model fine-tuning
    return {"status": "success", "message": "Feedback recorded for future model improvement."}

class JobResponse(BaseModel):
    job_id: str
    status: str

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    logger.info(f"User {form_data.username} logged in successfully.")
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/predict", response_model=JobResponse)
async def predict(
    image: UploadFile = File(...),
    clinical_notes: str = Form(...),
    prior_image: Optional[UploadFile] = File(None),
    window_center: Optional[int] = Form(None),
    window_width: Optional[int] = Form(None),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"User {current_user.username} submitted a prediction job.")
    
    image_content = await image.read()
    image_b64 = base64.b64encode(image_content).decode()
    
    prior_b64 = None
    if prior_image:
        prior_content = await prior_image.read()
        prior_b64 = base64.b64encode(prior_content).decode()
    
    task = predict_task.delay(
        image_b64, 
        clinical_notes, 
        prior_image_data_b64=prior_b64,
        window_center=window_center,
        window_width=window_width
    )
    
    return {"job_id": task.id, "status": "PENDING"}

@app.get("/status/{job_id}")
async def get_status(job_id: str, current_user: User = Depends(get_current_user)):
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

# Phase 3: Mock FHIR/EHR Integration Endpoints
@app.get("/fhir/Patient/{patient_id}/Observation")
async def get_patient_observations(patient_id: str, current_user: User = Depends(get_current_user)):
    """Mock endpoint to simulate pulling clinical data from an EHR."""
    logger.info(f"User {current_user.username} requested FHIR observations for patient {patient_id}")
    return {
        "resourceType": "Bundle",
        "entry": [
            {
                "resource": {
                    "resourceType": "Observation",
                    "status": "final",
                    "code": {"text": "Clinical Notes"},
                    "valueString": "Persistent cough, fever for 3 days, decreased breath sounds in right lower lobe."
                }
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
