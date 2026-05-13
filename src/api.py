from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import Response
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
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# Configure Logging
logging.basicConfig(
    filename="audit.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("Clinica-LENS-Audit")

# Metrics
REQUEST_COUNT = Counter("api_requests_total", "Total count of requests", ["method", "endpoint", "status", "tenant_id"])
REQUEST_LATENCY = Histogram("api_request_latency_seconds", "Request latency", ["method", "endpoint", "tenant_id"])

app = FastAPI(title="Clinica-LENS: Ultra-Enterprise Edition", description="Multi-tenant Production API for Clinical Excellence")

# Middleware for Audit Logging & Metrics
@app.middleware("http")
async def audit_log_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # Attempt to get tenant_id for granular metrics (simplified for demo)
    tenant_id = "unknown"
    if "Authorization" in request.headers:
        # In a real system, we'd decode the JWT here to get the tenant_id without full validation for metrics
        tenant_id = "authenticated_user" 

    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path, status=response.status_code, tenant_id=tenant_id).inc()
    REQUEST_LATENCY.labels(method=request.method, endpoint=request.url.path, tenant_id=tenant_id).observe(process_time)
    
    logger.info(f"Tenant: {tenant_id} Method: {request.method} Path: {request.url.path} Status: {response.status_code} Duration: {process_time:.4f}s")
    return response

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

# --- Models ---

class FeedbackRequest(BaseModel):
    job_id: str
    rating: int # 1 to 5
    comments: Optional[str] = None
    radiologist_override: Optional[str] = None

class JobResponse(BaseModel):
    job_id: str
    status: str

# Phase 5: FHIR DiagnosticReport Model
class FHIRDiagnosticReport(BaseModel):
    resourceType: str = "DiagnosticReport"
    status: str = "final"
    code: dict
    subject: dict
    effectiveDateTime: str
    issued: str
    performer: List[dict]
    result: List[dict]
    conclusion: str

# --- Endpoints ---

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
    logger.info(f"User {form_data.username} [Tenant: {user.tenant_id}] logged in successfully.")
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
    logger.info(f"Tenant: {current_user.tenant_id} | User {current_user.username} submitted a prediction job.")
    
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
    # In a real system, we'd verify that the task belongs to the user's tenant here
    if task_result.status == 'PENDING':
        return {"job_id": job_id, "status": "PENDING"}
    elif task_result.status == 'SUCCESS':
        return {"job_id": job_id, "status": "SUCCESS", "result": task_result.result}
    elif task_result.status == 'FAILURE':
        return {"job_id": job_id, "status": "FAILURE", "error": str(task_result.info)}
    return {"job_id": job_id, "status": task_result.status}

@app.post("/feedback")
async def submit_feedback(feedback: FeedbackRequest, current_user: User = Depends(get_current_user)):
    logger.info(f"Tenant: {current_user.tenant_id} | User {current_user.username} submitted feedback for job {feedback.job_id}.")
    return {"status": "success", "message": "Feedback recorded for future model improvement."}

# Phase 5: FHIR EHR Write-Back Endpoint
@app.post("/fhir/DiagnosticReport")
async def push_diagnostic_report(report: FHIRDiagnosticReport, current_user: User = Depends(get_current_user)):
    """Enterprise Write-Back: Push AI findings to hospital EHR."""
    logger.info(f"Tenant: {current_user.tenant_id} | User {current_user.username} pushing FHIR DiagnosticReport for Patient {report.subject.get('reference')}")
    # Simulating transmission to EHR (Epic/Cerner)
    return {"status": "success", "fhir_id": "report_123", "message": "Report successfully transmitted to EHR."}

# Phase 7: DICOMweb WADO-RS Stub
@app.get("/dicomweb/studies/{study_uid}")
async def get_study_metadata(study_uid: str, current_user: User = Depends(get_current_user)):
    """Modern DICOMweb: Retrieve study metadata via REST."""
    logger.info(f"Tenant: {current_user.tenant_id} | User {current_user.username} accessing DICOMweb Study {study_uid}")
    return {
        "0020000D": {"vr": "UI", "Value": [study_uid]},
        "00080060": {"vr": "CS", "Value": ["DX"]},
        "00100010": {"vr": "PN", "Value": [{"Alphabetic": "ANONYMOUS"}]}
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

# Phase 3: Mock FHIR/EHR Integration Endpoints
@app.get("/fhir/Patient/{patient_id}/Observation")
async def get_patient_observations(patient_id: str, current_user: User = Depends(get_current_user)):
    logger.info(f"Tenant: {current_user.tenant_id} | User {current_user.username} requested FHIR observations for patient {patient_id}")
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
