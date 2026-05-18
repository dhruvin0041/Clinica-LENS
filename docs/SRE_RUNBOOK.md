# SRE Runbook: Clinica-LENS

## Incident: High API Latency (> 2000ms)
**Symptoms:** 
- Datadog/Prometheus alerts on `api_request_latency_seconds`.
- Users report slow image uploads.

**Immediate Actions:**
1. Check HPA status: `kubectl get hpa -n production`. Ensure pods are scaling.
2. Check Redis Queue Depth: Connect to Redis and run `LLEN celery`. If depth > 1000, GPU workers are bottlenecked.
3. Scale Workers: `kubectl scale deployment clinica-lens-worker --replicas=10 -n production`.

## Incident: Orthanc DICOM Ingestion Failure
**Symptoms:**
- Orthanc logs show C-STORE failures.
- No new messages on `dicom_inbound_queue`.

**Immediate Actions:**
1. Check Orthanc Disk Space: `kubectl exec -it <orthanc-pod> -- df -h`.
2. Verify Network Policies: Ensure port 4242 is open from the hospital VPN/Gateway.
3. Check mTLS certificates: Verify `/etc/orthanc/certs/` for expiration.

## Incident: Out of Memory (OOMKilled) on Workers
**Symptoms:**
- Pods crashlooping with OOMKilled.

**Immediate Actions:**
1. Check DICOM size: Extremely large multi-frame series may exceed 4Gi limits.
2. Update memory limits in `k8s/production-deployment.yaml` and reapply.
