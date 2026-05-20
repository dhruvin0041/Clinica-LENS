import pytest
from unittest.mock import patch, MagicMock
from src.api import app, get_current_user
from fastapi.testclient import TestClient

client = TestClient(app)

# Override authentication for all tests in this file
app.dependency_overrides[get_current_user] = lambda: MagicMock(tenant_id="test_tenant", username="test_user")

@patch("src.api.authenticate_user")
def test_login_success(mock_authenticate):
    mock_user = MagicMock()
    mock_user.username = "testuser"
    mock_user.tenant_id = "test_tenant"
    mock_authenticate.return_value = mock_user

    response = client.post("/token", data={"username": "testuser", "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()

@patch("src.api.authenticate_user")
def test_login_failure(mock_authenticate):
    mock_authenticate.return_value = False
    
    response = client.post("/token", data={"username": "wrong", "password": "wrong"})
    assert response.status_code == 401

@patch("src.api.AsyncResult")
def test_get_status_pending(mock_async_result):
    mock_result = MagicMock()
    mock_result.status = "PENDING"
    mock_async_result.return_value = mock_result
    
    response = client.get("/status/123", headers={"Authorization": "Bearer fake"})
    assert response.status_code == 200
    assert response.json() == {"job_id": "123", "status": "PENDING"}

@patch("src.api.AsyncResult")
def test_get_status_success(mock_async_result):
    mock_result = MagicMock()
    mock_result.status = "SUCCESS"
    mock_result.result = {"prediction": 1}
    mock_async_result.return_value = mock_result
    
    response = client.get("/status/123", headers={"Authorization": "Bearer fake"})
    assert response.status_code == 200
    assert response.json() == {"job_id": "123", "status": "SUCCESS", "result": {"prediction": 1}}

def test_submit_feedback():
    response = client.post(
        "/feedback", 
        json={"job_id": "123", "rating": 5, "comments": "Good"},
        headers={"Authorization": "Bearer fake"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_push_diagnostic_report():
    report_data = {
        "resourceType": "DiagnosticReport",
        "status": "final",
        "code": {"text": "Chest X-ray"},
        "subject": {"reference": "Patient/123"},
        "effectiveDateTime": "2023-10-27T10:00:00Z",
        "issued": "2023-10-27T10:05:00Z",
        "performer": [{"reference": "Practitioner/AI"}],
        "result": [],
        "conclusion": "Normal"
    }
    response = client.post(
        "/fhir/DiagnosticReport",
        json=report_data,
        headers={"Authorization": "Bearer fake"}
    )
    assert response.status_code == 200
    assert response.json()["fhir_id"] == "report_123"

def test_get_study_metadata():
    response = client.get("/dicomweb/studies/1.2.3", headers={"Authorization": "Bearer fake"})
    assert response.status_code == 200
    assert "0020000D" in response.json()

def test_get_patient_observations():
    response = client.get("/fhir/Patient/123/Observation", headers={"Authorization": "Bearer fake"})
    assert response.status_code == 200
    assert response.json()["resourceType"] == "Bundle"

def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "api_requests_total" in response.text
