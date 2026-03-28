---

# 🚀 Cross-Cloud SOC Auto-Remediation System

**Production-Grade Cloud Security Automation (Azure + AWS)**

## > ⚡ Detect → Respond → Remediate in **< 30 seconds**
## > 🔐 Zero human intervention | 100% detection | 0% false positives

---

## 📌Cross-Cloud SOC Auto-Remediation System  (Overview)

This project demonstrates a **real-world, production-grade SOC automation system** that integrates **Microsoft Sentinel (Azure)** with **AWS serverless services** to automatically detect and remediate security threats.

When a threat is detected:

1. Microsoft Sentinel creates an incident
2. Azure Logic Apps triggers automation
3. AWS Lambda executes remediation
4. IAM threats are neutralized instantly

---

## 🏆 Key Achievements

* ✅ **100% Detection Rate** across 5 attack scenarios
* ✅ **0% False Positives**
* ⚡ **< 30 Seconds Response Time**
* 🔄 Fully automated **cross-cloud remediation**
* 🔐 Implemented **IAM least privilege & OIDC federation**
* 🧠 Built **idempotent, fault-tolerant serverless system**

---

## 🧱 Architecture

```
Attacker → AWS CloudTrail → Sentinel (Azure)
        → KQL Detection Rule → Incident Created
        → Logic App → API Gateway → Lambda
        → IAM Remediation → SES Alert → Sentinel Update
```

### 🔁 End-to-End Flow

1. Suspicious IAM activity detected
2. Logs ingested into Sentinel via OIDC
3. KQL rule triggers incident
4. Logic App sends request to AWS
5. API Gateway invokes Lambda
6. Lambda disables IAM keys
7. Alert sent via SES
8. Audit trail written back to Sentinel

---

## 🛠️ Tech Stack

| Layer      | Technology               |
| ---------- | ------------------------ |
| SIEM       | Microsoft Sentinel       |
| Detection  | KQL                      |
| Automation | Azure Logic Apps         |
| Compute    | AWS Lambda (Python 3.12) |
| API        | AWS API Gateway          |
| Identity   | AWS IAM                  |
| Email      | Amazon SES               |
| Storage    | DynamoDB                 |
| Logs       | CloudTrail + CloudWatch  |
| Auth       | OIDC Federation          |

---

## 🔍 Detection Engineering

Built **5 production-grade analytics rules** mapped to **MITRE ATT&CK**:

* Privilege Escalation (T1078)
* Brute Force (T1110)
* Mass Resource Deployment
* Suspicious Storage Creation
* Malicious Blob Upload (C2 / Phishing)

---

## 🎯 Attack Simulations

| Scenario               | Result     |
| ---------------------- | ---------- |
| Privilege Escalation   | ✅ Detected |
| Brute Force Attack     | ✅ Detected |
| Mass Resource Creation | ✅ Detected |
| Suspicious Storage     | ✅ Detected |
| Phishing/C2 Hosting    | ✅ Detected |

> 🔥 **Detection Rate: 100% | False Positives: 0%**

---

## 🧠 Core Engineering Highlights

### 🔐 Cross-Cloud Security Automation

* Azure Sentinel → AWS Lambda integration
* Secure communication via API Gateway + IAM

### ⚙️ Idempotency (Critical Design Pattern)

* DynamoDB prevents duplicate execution
* Ensures safe and consistent remediation

### 🛡️ IAM Threat Containment

* Automatically disables compromised access keys
* Enforces tag-based least privilege

### 🔄 Fail-Safe Mechanisms

* Circuit breaker to disable automation instantly
* Retry logic with exponential backoff
* CloudWatch alerts for failure monitoring

---

## 🧪 Testing & Validation

✔ CloudTrail logs ingested
✔ Sentinel incidents created
✔ Logic App triggered
✔ Lambda executed successfully
✔ IAM keys disabled
✔ Email alerts delivered
✔ Idempotency verified

---

## 📊 Metrics

| Metric          | Value    |
| --------------- | -------- |
| Detection Rate  | 100%     |
| False Positives | 0%       |
| Response Time   | < 30 sec |
| Incidents       | 2        |
| Events Analyzed | 87       |

---

## 🔎 Incident Response (Real Simulation)

### 🚨 Multi-Stage Attack (CRITICAL)

* Duration: 11+ hours
* Phases: Recon → Priv Esc → Deploy → Persist → Cleanup
* Root Cause: No MFA + excessive privileges

### ✅ Actions Taken

* Disabled compromised account
* Revoked sessions
* Removed malicious infrastructure

---

## 💬 Interview Talking Point

> “I built a cross-cloud SOC system where Microsoft Sentinel detects threats and automatically triggers AWS Lambda to remediate IAM attacks in under 30 seconds, with zero human intervention.”

---

## 📈 Why my Project Stands Out

This is **not a basic lab** — it demonstrates:

* Real-world SOC workflows
* Cross-cloud architecture
* Security automation at scale
* Production-ready engineering practices
* Deep understanding of cloud security

---

## 🚀 Future Improvements

* Infrastructure as Code (Terraform)
* CI/CD pipeline (GitHub Actions)
* Multi-region failover
* Slack / Teams integration
* ML-based anomaly detection

---

## 📎 Project Structure

```
/kql-rules
/lambda-function
/logic-app
/architecture
/docs
```
## 🛡️ Security Engineering Highlights

- OIDC cross-cloud authentication (no static credentials)
- Idempotency using DynamoDB
- Circuit breaker fail-safe mechanism
- Tag-based IAM least privilege
- Input validation + retry logic
- CloudWatch metrics & alerting
---


## 👤 Author

**MUSA OLALEKAN (Sir Lakewest)**

---

## 📌 License

MIT License# Cross-Cloud-Auto-Detection-Remediation
# Cross-Cloud-Auto-Detection-Remediation
# Cross-Cloud-SOC-Automation-Remediation-v2
