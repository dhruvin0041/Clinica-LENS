# Disaster Recovery Strategy: Clinica-LENS

## RTO & RPO Objectives
- **RTO (Recovery Time Objective):** 1 Hour
- **RPO (Recovery Point Objective):** 15 Minutes

## Backups
- **AWS S3 (DICOM & Models):** Versioning enabled. Cross-region replication to `us-west-2`.
- **Redis (Task Queue):** Redis Append Only File (AOF) enabled. Nightly snapshots to S3.
- **Orthanc DB (PostgreSQL/SQLite):** Nightly dumps.

## Restore Procedure (Total Cluster Loss)
1. **Infrastructure:** Apply Terraform to a new AWS region: `terraform apply -var="aws_region=us-west-2"`.
2. **State Retrieval:** Point the new cluster to the replicated S3 bucket.
3. **Application Deploy:** Run the GitHub Actions CI/CD pipeline targeting the new EKS cluster.
4. **DNS Failover:** Update Route53 to point to the new Ingress Controller LoadBalancer.
