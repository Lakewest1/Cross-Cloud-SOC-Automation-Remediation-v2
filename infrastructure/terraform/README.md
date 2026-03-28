# Terraform (Light Infrastructure)

This Terraform setup provisions core AWS resources for the SOC Auto-Remediation system.

## Resources Created
- AWS Lambda (Remediation Engine)
- DynamoDB (Idempotency Table)
- IAM Role (Least privilege execution)

## 🚀 Deploy

```bash
terraform init
terraform apply