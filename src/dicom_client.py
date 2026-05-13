import logging
from pynetdicom import AE, StorageSOPClassList
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelFind, PatientRootQueryRetrieveInformationModelMove
from pydicom.dataset import Dataset

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DICOM-Client")

class PACSClient:
    """
    Active DICOM Client (SCU) for querying and retrieving historical scans.
    Enables Clinica-LENS to pull prior studies for longitudinal analysis.
    """
    def __init__(self, pacs_ip, pacs_port, pacs_ae="HOSPITAL_PACS", local_ae="CLINICA_LENS"):
        self.pacs_ip = pacs_ip
        self.pacs_port = pacs_port
        self.pacs_ae = pacs_ae
        self.local_ae = local_ae
        self.ae = AE(ae_title=local_ae)
        
        # Add presentation contexts for Find and Move
        self.ae.add_requested_context(PatientRootQueryRetrieveInformationModelFind)
        self.ae.add_requested_context(PatientRootQueryRetrieveInformationModelMove)
        
        # Add all storage classes for receiving (required for C-MOVE)
        for sop_class in StorageSOPClassList:
            self.ae.add_requested_context(sop_class)

    def find_prior_studies(self, patient_id):
        """Perform a C-FIND to search for patient studies."""
        ds = Dataset()
        ds.PatientID = patient_id
        ds.QueryRetrieveLevel = "STUDY"
        ds.StudyInstanceUID = ""
        ds.StudyDate = ""
        ds.StudyDescription = ""
        
        logger.info(f"Querying PACS {self.pacs_ae} for PatientID: {patient_id}")
        
        assoc = self.ae.associate(self.pacs_ip, self.pacs_port, ae_title=self.pacs_ae)
        studies = []
        if assoc.is_established:
            responses = assoc.send_c_find(ds, PatientRootQueryRetrieveInformationModelFind)
            for (status, identifier) in responses:
                if status and status.Status == 0xFF00: # Pending (Success)
                    studies.append(identifier)
            assoc.release()
            logger.info(f"Found {len(studies)} historical studies.")
        else:
            logger.error("Failed to establish association for C-FIND.")
        
        return studies

    def retrieve_study(self, study_instance_uid, dest_ae="CLINICA_LENS"):
        """Perform a C-MOVE to retrieve a specific study."""
        ds = Dataset()
        ds.QueryRetrieveLevel = "STUDY"
        ds.StudyInstanceUID = study_instance_uid
        
        logger.info(f"Requesting C-MOVE for Study: {study_instance_uid} to {dest_ae}")
        
        assoc = self.ae.associate(self.pacs_ip, self.pacs_port, ae_title=self.pacs_ae)
        if assoc.is_established:
            responses = assoc.send_c_move(ds, dest_ae, PatientRootQueryRetrieveInformationModelMove)
            for (status, identifier) in responses:
                if status:
                    logger.info(f"C-MOVE Status: {status.Status}")
            assoc.release()
        else:
            logger.error("Failed to establish association for C-MOVE.")

if __name__ == "__main__":
    # Example usage (simulated)
    client = PACSClient("127.0.0.1", 11112)
    # studies = client.find_prior_studies("PATIENT_001")
    # if studies:
    #     client.retrieve_study(studies[0].StudyInstanceUID)
