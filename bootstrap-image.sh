#!/usr/bin/env bash
# First deploy only: push a "bootstrap" image so the service has something to run.
# After this, every merge to main deploys through GitHub Actions.
set -euo pipefail
REGION=${AWS_REGION:-us-east-1}
REPO=$(cd infra && terraform output -raw ecr_repository_url)
aws ecr get-login-password --region "$REGION" | docker login --username AWS --password-stdin "${REPO%/*}"
docker build -t "$REPO:bootstrap" .
docker push "$REPO:bootstrap"
echo "Pushed $REPO:bootstrap. Now run: cd infra && terraform apply"
