# 🧠 Design Decisions

## Why Lambda?
- Native AWS access (no complex auth)
- Scalable + serverless
- Supports retry + validation

## Why DynamoDB?
- Enables idempotency
- Prevents duplicate remediation

## Why API Gateway?
- Secure entry point
- IAM authentication

## Why Logic Apps?
- Easy orchestration across services
- Native Sentinel integration