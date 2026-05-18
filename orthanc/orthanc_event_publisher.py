import orthanc
import redis
import json

# Orthanc Python Plugin to publish events to Redis on new instance
redis_client = redis.StrictRedis(host='redis-service', port=6379, db=0)

def OnStoredInstance(dicom, instanceId):
    # Anonymize tags before publishing
    tags = json.loads(dicom.GetInstanceSimplifiedJson())
    
    # Extract study/series details
    study_uid = tags.get("StudyInstanceUID", "")
    series_uid = tags.get("SeriesInstanceUID", "")
    
    event = {
        "event_type": "NEW_DICOM_INSTANCE",
        "instance_id": instanceId,
        "study_uid": study_uid,
        "series_uid": series_uid,
        "status": "ANONYMIZED_AND_READY"
    }
    
    # Publish to Redis Pub/Sub or a List queue
    redis_client.rpush("dicom_inbound_queue", json.dumps(event))
    orthanc.LogWarning(f"Published event to Redis for Instance {instanceId}")

orthanc.RegisterOnStoredInstanceCallback(OnStoredInstance)
