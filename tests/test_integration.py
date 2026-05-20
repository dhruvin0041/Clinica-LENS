import pytest
from fastapi.testclient import TestClient
from src.api import app, get_current_user
from unittest.mock import patch, MagicMock

# Bypass authentication for testing
app.dependency_overrides[get_current_user] = lambda: MagicMock(tenant_id="test_tenant", username="test_user")

client = TestClient(app)

@pytest.fixture
def mock_token():
    return "Bearer fake-jwt-token"

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@patch("src.api.predict_task.delay")
def test_predict_endpoint_stateless(mock_celery_delay):
    # Mock Celery Task
    mock_task = MagicMock()
    mock_task.id = "mock-task-123"
    mock_celery_delay.return_value = mock_task

    # Send a multipart request to /predict
    files = {'image': ('test.dcm', b'fake dicom bytes', 'application/dicom')}
    data = {'clinical_notes': 'Patient has a cough.'}
    
    response = client.post(
        "/predict",
        files=files,
        data=data,
        headers={"Authorization": "Bearer fake-jwt-token"}
    )
    
    assert response.status_code == 200
    assert response.json()["status"] == "PENDING"
    assert response.json()["job_id"] == "mock-task-123"
    
    # Verify Celery was called
    mock_celery_delay.assert_called()
