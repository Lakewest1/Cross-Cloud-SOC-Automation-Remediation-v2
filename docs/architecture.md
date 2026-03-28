# 🏗️ System Architecture

## 📌 Overview

This system connects Azure Sentinel and AWS to enable automated security response.

---

## 🔄 Flow Diagram

1. AWS CloudTrail logs event
2. Sentinel ingests logs (OIDC)
3. KQL detects anomaly
4. Incident created
5. Logic App triggers
6. API Gateway invoked
7. Lambda executes remediation
8. IAM actions performed
9. Email alert sent
10. Sentinel updated

---

## 📸 Diagrams

![Architecture](screenshots/architecture-diagram.png)
![Logic App](screenshots/logic-app-flow.png)