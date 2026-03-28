# ⚙️ Lambda Remediation Engine

## Purpose

Handles automated IAM remediation triggered by Sentinel.

---

## 🔧 Features

- Idempotency (DynamoDB)
- IAM key disablement
- SES email alerts
- Input validation
- Circuit breaker support

---

## 🚀 Run Locally

```bash
pip install -r requirements.txt
pytest


##📌 Environment Variables
ACCOUNT_ID
SES_FROM_EMAIL
IDEMPOTENCY_TABLE
AUTO_REMEDIATION