# Enterprise Security & Hardening

## 1. Mutual TLS (mTLS)
All internal service-to-service communication within the Kubernetes cluster is secured using a Service Mesh (Linkerd/Istio).
- **Annotation:** Deployments contain `linkerd.io/inject: enabled`.
- **DICOM TLS:** Orthanc enforces DICOM TLS requiring client certificates for all SCU associations.

## 2. Secrets Management
- No secrets are stored in Git.
- We utilize **AWS Secrets Manager** synced via the External Secrets Operator (ESO) into Kubernetes Secrets.

## 3. RBAC & Identity
- API endpoints authenticate via OIDC JWTs issued by Keycloak.
- Kubernetes administration is locked down via AWS IAM roles mapped to K8s RBAC groups.

## 4. Network Policies
- Zero-trust network policies are enforced. The API can only talk to Redis and S3. Orthanc can only talk to Redis. Egress to the internet is blocked except for required external APIs.
