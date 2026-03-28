##Manual Deployment:

Sentinel → Analytics → + Create → Scheduled query rule

Copy KQL from kql-rules/ directory

Configure:

Name: (from rule)

Description: MITRE mapping + business impact

Query: Paste KQL

Schedule: 5 minutes

Lookup data: Last 5 minutes

Severity: As defined

MITRE ATT&CK: Add tactics and techniques

Set Custom details for Lambda:

ThreatCategory

SourceIP

UserType

AWSRegion

ActionsDetected

Click Create

