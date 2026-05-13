import os
import logging
from pynetdicom import AE, evt, StorageSOPClassList
from pydicom.dataset import Dataset

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DICOM-Listener")

STORAGE_DIR = "data/dicom_inbox"
os.makedirs(STORAGE_DIR, exist_ok=True)

def handle_store(event):
    """Handle a C-STORE request event."""
    ds = event.dataset
    ds.file_meta = event.file_meta
    
    # Generate a filename (using SOP Instance UID)
    filename = os.path.join(STORAGE_DIR, f"{ds.SOPInstanceUID}.dcm")
    
    # Enterprise Requirement: De-identification (Basic)
    # In a real system, we'd use a more comprehensive de-identification profile
    ds.PatientName = "ANONYMOUS"
    ds.PatientID = "HIDDEN"
    ds.PatientBirthDate = ""
    
    ds.save_as(filename, write_like_original=False)
    logger.info(f"Received and saved DICOM: {filename}")
    
    # Return a 'Success' status
    return 0x0000

def start_listener(port=11112, ae_title=b"CLINICA_LENS"):
    ae = AE(ae_title=ae_title)
    
    # Add supported presentation contexts (Standard Storage)
    ae.supported_contexts = StorageSOPClassList
    
    handlers = [(evt.EVT_C_STORE, handle_store)]
    
    logger.info(f"Starting DICOM Listener on port {port} with AE Title {ae_title.decode()}...")
    # This blocks, so it should be run in a separate process or thread
    ae.start_server(("", port), evt_handlers=handlers)

if __name__ == "__main__":
    start_listener()
