import pytest
from fastapi.testclient import TestClient
from src.api import app
from unittest.mock import patch, MagicMock

client = TestClient(app)

@pytest.fixture
def mock_token():
    return "Bearer fake-jwt-token"

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@patch("src.api.StorageBackend")
@patch("src.api.predict_task.delay")
@patch("src.api.get_current_user")
def test_predict_endpoint_stateless(mock_get_user, mock_celery_delay, mock_storage):
    # Mock authentication
    mock_user = MagicMock()
    mock_user.tenant_id = "test_tenant"
    mock_user.username = "test_user"
    mock_get_user.return_value = mock_user

    # Mock S3 Storage
    mock_storage_instance = MagicMock()
    mock_storage_instance.upload_file.return_value = "s3://clinica-lens-data/mock_image.dcm"
    mock_storage.return_value = mock_storage_instance
    
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
    
    # Verify S3 upload was called
    mock_storage_instance.upload_file.assert_called()
    
    # Verify Celery was called with the S3 URI, not a local path or base64
    mock_celery_delay.assert_called_with(
        image_uri="s3://clinica-lens-data/mock_image.dcm",
        clinical_notes='Patient has a cough.',
        prior_image_uri=None,
        window_center=None,
        window_width=None
    )
