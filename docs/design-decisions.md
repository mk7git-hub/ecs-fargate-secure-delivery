# Design decisions: Secure Container Delivery

### 1. Fargate instead of ECS on EC2 or EKS
- **Why:** no hosts to patch or scale; right for a small stateless service. EKS adds a control-plane cost and complexity this service does not need.

### 2. Private subnets with VPC endpoints instead of NAT
- **Why:** tasks need only ECR, S3 (image layers) and CloudWatch Logs. Endpoints keep traffic on the AWS network; no internet path for a compromised task.
- **Trade-off:** each interface endpoint costs per AZ-hour; at more than about four endpoints a NAT can be cheaper, but it reopens internet egress.

### 3. Trivy gate with `ignore-unfixed`
- **Why:** fail on vulnerabilities that have a fix available; unfixed ones are tracked in SARIF but don't block shipping forever.

### 4. Immutable tags equal to the commit SHA
- **Why:** an image tag can never be overwritten, so what's running is traceable to exact code. `latest` is ambiguous.

### 5. Circuit breaker with rollback, 100/200 deployment percentages
- **Why:** new tasks must pass health checks before old ones stop; failures revert automatically.

### 6. Hardened task definition
- Read-only root filesystem, all capabilities dropped, non-root user, init process for signal handling, no task role permissions (the app calls no AWS APIs).

### 7. Terraform owns infrastructure, the pipeline owns the running image
- **Why:** `ignore_changes = [task_definition]` stops Terraform from rolling back the image the pipeline deployed. Clear ownership avoids fights between tools.

### 8. Standard-library app
- **Why:** a tiny dependency surface keeps the scan meaningful; the project is about delivery, not the app.

### 9. HTTP-only ALB in the lab
- **Why:** HTTPS needs a domain and certificate. The README documents the ACM certificate and redirect change.
