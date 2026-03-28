# Threat Model: STRIDE Analysis

## System Boundaries
- **Azure Side**: Sentinel, Logic Apps, Azure AD
- **AWS Side**: Lambda, API Gateway, IAM, SES, DynamoDB
- **Cross-Cloud**: OIDC Federation, HTTPS API calls

---

## STRIDE Analysis

### S - Spoofing

| Threat | Description | Mitigation |
|--------|--------------|------------|
| **Fake CloudTrail Events** | Attacker injects false events into Sentinel | OIDC authentication, least-privilege IAM |
| **API Gateway Impersonation** | Malicious actor calls API Gateway | AWS_IAM auth with Signature V4 |
| **Logic App Spoofing** | Unauthorized Logic App calls Sentinel | Managed Identity, role assignments |

### T - Tampering

| Threat | Description | Mitigation |
|--------|--------------|------------|
| **Log Modification** | CloudTrail logs altered before ingestion | AWS S3 server-side encryption, SQS DLQ |
| **Lambda Code Injection** | Attacker modifies function code | IAM least privilege, code signing |
| **DynamoDB Record Tampering** | Idempotency records corrupted | Conditional writes, TTL auto-delete |

### R - Repudiation

| Threat | Description | Mitigation |
|--------|--------------|------------|
| **Deny of Action** | Attacker denies performing IAM actions | CloudTrail audit logs, Sentinel incident comments |
| **No Remediation Proof** | Unable to prove auto-remediation | Lambda logs, SES email, Sentinel comments |

### I - Information Disclosure

| Threat | Description | Mitigation |
|--------|--------------|------------|
| **SES Email Interception** | Alert emails read by attacker | TLS encryption, verified identities only |
| **Lambda Environment Variables** | Secrets exposed in logs | No secrets in env vars, use Secrets Manager |
| **API Gateway Logs** | Sensitive incident data in logs | Disable request/response logging for sensitive fields |

### D - Denial of Service

| Threat | Description | Mitigation |
|--------|--------------|------------|
| **Lambda Throttling** | Too many concurrent invocations | Reserved concurrency (10), DLQ |
| **DynamoDB Throttling** | Write capacity exhausted | On-demand capacity, exponential backoff |
| **SES Rate Limiting** | Email sending blocked | Verified identities, sandbox mode, retries |
| **Sentinel Overload** | Too many incidents created | Deduplication via idempotency, incident grouping |

### E - Elevation of Privilege

| Threat | Description | Mitigation |
|--------|--------------|------------|
| **Lambda Escalation** | Lambda disables wrong IAM user | Tag-based condition `ManagedBy=Sentinel` |
| **API Gateway Bypass** | Direct Lambda invocation | Resource-based policy on Lambda |
| **Logic App Over-Privilege** | Playbook accesses unintended resources | Managed Identity with least-privilege roles |

---

## Data Flow Threats

### Step 1: CloudTrail → Sentinel (OIDC)

| Threat | Mitigation |
|--------|------------|
| OIDC token interception | HTTPS, token expiration (1 hour) |
| Unauthorized connector | IAM role condition on AWS side |
| Log delivery failure | SQS DLQ, CloudWatch alarm |

### Step 2: Sentinel → Logic App

| Threat | Mitigation |
|--------|------------|
| Automation rule bypass | Role assignment verification |
| Playbook execution failure | Retry policy, manual override |

### Step 3: Logic App → API Gateway

| Threat | Mitigation |
|--------|------------|
| Intercepted HTTP request | TLS 1.3, AWS_IAM auth |
| Malformed payload | JSON schema validation in Lambda |
| Replay attack | Idempotency with DynamoDB |

### Step 4: API Gateway → Lambda

| Threat | Mitigation |
|--------|------------|
| Unauthorized invocation | Resource-based policy, allowed ARNs |
| Cold start delay | Provisioned concurrency (optional) |
| Lambda timeout | 30s timeout with CloudWatch alarm |

### Step 5: Lambda → IAM

| Threat | Mitigation |
|--------|------------|
| Key disable for wrong user | Tag-based condition |
| IAM API throttling | Exponential backoff |
| Insufficient permissions | IAM policy review, least privilege |

### Step 6: Lambda → SES

| Threat | Mitigation |
|--------|------------|
| Email to unverified address | SES sandbox, verified identities only |
| Email content spoofing | DKIM signing (recommended) |
| SES sending limits | Sandbox mode limits, request production access |

### Step 7: Lambda → DynamoDB

| Threat | Mitigation |
|--------|------------|
| Duplicate writes | Conditional write with `attribute_not_exists` |
| Table not found | CloudFormation, automated deployment |
| TTL not set | 90-day TTL with `ttl` attribute |

---

## Risk Matrix

| Threat | Likelihood | Impact | Risk Level | Mitigation |
|--------|------------|--------|------------|------------|
| Account compromise | Medium | Critical | High | MFA, Conditional Access |
| Lambda privilege escalation | Low | Critical | Medium | Tag-based IAM condition |
| API Gateway bypass | Low | High | Low | Resource-based policy |
| Idempotency failure | Low | Medium | Low | DynamoDB conditional writes |
| Log ingestion delay | Medium | Medium | Medium | CloudWatch alarms, SQS DLQ |

---

## Security Controls Summary

| Control | Implementation | Coverage |
|---------|----------------|----------|
| Authentication | OIDC, AWS_IAM | Cross-cloud |
| Authorization | IAM policies, tag conditions | AWS side |
| Encryption | TLS 1.3, S3 SSE | In transit & at rest |
| Logging | CloudTrail, Sentinel, CloudWatch | Full audit trail |
| Monitoring | CloudWatch alarms, Sentinel incidents | Real-time |
| Incident Response | Auto-remediation, manual override | <30s |
| Idempotency | DynamoDB conditional writes | Duplicate prevention |
| Circuit Breaker | Environment variable | Instant kill switch |

---

## Penetration Testing Results

| Test | Result | Notes |
|------|--------|-------|
| SQL Injection in Lambda | ✅ Blocked | Input validation, JSON parsing |
| XSS in SES Email | ✅ Blocked | HTML escaping |
| API Gateway Flood | ✅ Mitigated | AWS Shield, throttling |
| Lambda Over-invocation | ✅ Controlled | Reserved concurrency (10) |
| Unauthorized IAM Disable | ✅ Blocked | Tag condition `ManagedBy=Sentinel` |
| Idempotency Bypass | ✅ Blocked | Conditional write atomic |
| Circuit Breaker Test | ✅ Working | `AUTO_REMEDIATION=false` |

---

## Continuous Improvement

### Quarterly Review
- Update threat model with new attack vectors
- Review IAM policies for least privilege
- Test circuit breaker in production
- Validate idempotency for new incident types

### Annual Penetration Test
- Full red team exercise
- Cross-cloud attack simulation
- Fail-safe mechanism validation

## 🎯 Threats Covered

- Privilege Escalation
- Credential Abuse
- Resource Hijacking
- Data Exfiltration
- Command & Control Hosting

---

## 🧠 MITRE ATT&CK Mapping

- T1078 – Valid Accounts
- T1110 – Brute Force
- T1583 – Resource Development
- T1102 – Web Service (C2)

---

## 🔐 Security Controls

- Detection: KQL analytics rules
- Prevention: IAM least privilege
- Response: Lambda remediation
- Monitoring: CloudWatch + Sentinel

