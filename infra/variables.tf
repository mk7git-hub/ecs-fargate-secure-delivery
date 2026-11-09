variable "region" {
  type    = string
  default = "us-east-1"
}

variable "owner" { type = string }

variable "github_repo" {
  type        = string
  description = "owner/repo allowed to push images and deploy, e.g. mk7git-hub/ecs-fargate-secure-delivery"
}

variable "image_tag" {
  type        = string
  default     = "bootstrap"
  description = "Image tag for the first deploy; the pipeline sets later tags"
}

variable "allowed_cidr" {
  type        = string
  default     = "0.0.0.0/0"
  description = "Who can reach the ALB. Set to your IP/32 to keep the demo private."
}

variable "github_owner_id" {
  type        = number
  description = "Numeric GitHub owner ID (OIDC subjects include it for repos created after July 2026)"
}

variable "github_repo_id" {
  type        = number
  description = "Numeric GitHub repository ID"
}
