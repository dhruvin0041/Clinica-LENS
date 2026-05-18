import os
import json
import logging
import redis
from celery import Celery
from opentelemetry import trace

logger = logging.getLogger("DICOM-Event-Adapter")
logger.setLevel(logging.INFO)

redis_client = redis.StrictRedis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True
)

celery_app = Celery("clinica_lens_worker", broker=os.getenv("CELERY_BROKER_URL"))

def listen_for_events():
    logger.info("Starting Event-Driven DICOM Adapter...")
    tracer = trace.get_tracer(__name__)
    
    while True:
        try:
            # Blocking pop from Redis queue
            queue, message = redis_client.blpop("dicom_inbound_queue", timeout=0)
            event = json.loads(message)
            
            with tracer.start_as_current_span("Process Inbound DICOM Event") as span:
                instance_id = event.get("instance_id")
                study_uid = event.get("study_uid")
                
                span.set_attribute("dicom.instance_id", instance_id)
                span.set_attribute("dicom.study_uid", study_uid)
                
                logger.info(f"Received DICOM event for Instance {instance_id}")
                
                # Retrieve from Orthanc via REST API
                # Orthanc -> S3 -> Celery
                # (Simulated logic for bridging)
                # s3_uri = orthanc_to_s3(instance_id)
                
                # Dispatch downstream inference
                # celery_app.send_task("tasks.predict_task", kwargs={"image_uri": s3_uri})
                
        except Exception as e:
            logger.error(f"Error processing event: {e}")

if __name__ == "__main__":
    listen_for_events()
