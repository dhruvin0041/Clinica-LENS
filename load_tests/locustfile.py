from locust import HttpUser, task, between

class ClinicaLensLoadTest(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        # Authenticate and get JWT
        response = self.client.post("/token", data={"username": "radiologist1", "password": "clinica-lens-2026"})
        if response.status_code == 200:
            self.token = response.json().get("access_token")
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            self.token = None
            self.headers = {}

    @task(3)
    def check_health(self):
        self.client.get("/health")

    @task(1)
    def submit_prediction(self):
        if not self.token:
            return
            
        # Simulate DICOM upload
        files = {'image': ('dummy.dcm', b'fake dicom payload', 'application/dicom')}
        data = {'clinical_notes': 'Routine screening'}
        
        self.client.post("/predict", files=files, data=data, headers=self.headers)
