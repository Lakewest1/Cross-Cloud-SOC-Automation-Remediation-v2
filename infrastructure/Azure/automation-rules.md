## AUTOMATION
Portal Method:

Sentinel → Automation → + Create → Automation rule

Name: Auto-Respond-to-High-Risk-Incidents

Trigger: When an incident is created

Conditions:

Severity: High

Status: New

Actions:

Change status to In Progress

Assign owner: security@company.com

Add tag: critical-incident

Run playbook: Critical-Incident-Email-Alert

Click Create

Create Logic App Playbook
Portal Method:

Sentinel → Automation → + Create → Playbook with incident trigger

Configure:

Name: Critical-Incident-Email-Alert

Subscription: Your subscription

Resource group: SOC-lab-01

Region: East US

Workspace: soclawlab

Click Create

Configure Email Action
In Logic App Designer, click + New step

Search "send an email"

Select Send an email (V2) (Office 365 Outlook)

Configure:

To: ir-responder@gmail.com, olamilake95@gmail.com

Subject: 🚨 CRITICAL INCIDENT - @{triggerBody()?['object/properties/title']}

Body:

text
Incident Alert: @{triggerBody()?['object/properties/title']}
Severity: @{triggerBody()?['object/properties/severity']}
Status: @{triggerBody()?['object/properties/status']}
Created: @{triggerBody()?['object/properties/createdTimeUtc']}
Incident ID: @{triggerBody()?['object/properties/incidentNumber']}

IMMEDIATE ACTION REQUIRED!
Add Cross-Cloud HTTP Action
Click + New step

Search "HTTP"

Select HTTP

Configure:

Method: POST

URI: https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/prod/remediate

Headers: Content-Type: application/json

Body:

json
{
  "incident_id": "@{triggerBody()?['object']?['properties']?['incidentNumber']}",
  "incident_type": "@{triggerBody()?['object']?['properties']?['title']}",
  "severity": "@{triggerBody()?['object']?['properties']?['severity']}",
  "threat_type": "@{triggerBody()?['object']?['properties']?['additionalData']?['customDetails']?['ThreatCategory'][0]}",
  "source_ip": "@{triggerBody()?['object']?['properties']?['additionalData']?['customDetails']?['SourceIP'][0]}",
  "username": "@{triggerBody()?['object']?['properties']?['additionalData']?['customDetails']?['UserType'][0]}",
  "aws_region": "@{triggerBody()?['object']?['properties']?['additionalData']?['customDetails']?['AWSRegion'][0]}",
  "actions_detected": "@{triggerBody()?['object']?['properties']?['additionalData']?['customDetails']?['ActionsDetected'][0]}"
}
Add condition after HTTP:

Condition: @equals(triggerBody()?['statusCode'], 200)

True: Add comment with Lambda response

False: Add failure comment

Assign Role Permissions
Sentinel incident page → Add role assignment

Role: Microsoft Sentinel Automation Contributor

Member: Your name

Click Review + assign

 Workbooks Configuration
Create Security Dashboard
Portal Method:

Sentinel → Workbooks → + Add workbook

Add queries:

kql
// Query 1: Incident Overview
SecurityIncident
| where TimeGenerated > ago(7d)
| summarize Count = count() by Severity
| render piechart

// Query 2: Incident Trend
SecurityIncident
| where TimeGenerated > ago(14d)
| summarize Count = count() by bin(TimeGenerated, 1d)
| render timechart

// Query 3: Detection Sources
SecurityIncident
| where TimeGenerated > ago(7d)
| summarize Count = count() by ProviderName
| render barchart

// Query 4: Auto-Remediation Success Rate
SecurityIncident
| where TimeGenerated > ago(30d)
| extend AutoRemediated = iff(Comments contains "remediation", "Yes", "No")
| summarize Count = count() by AutoRemediated
| render piechart

// Query 5: Response Time
SecurityIncident
| where TimeGenerated > ago(7d)
| extend ResponseTime = datetime_diff('second', FirstActivityTime, TimeGenerated)
| summarize AvgResponse = avg(ResponseTime), P95Response = percentile(ResponseTime, 95)
Save as Cross-Cloud SOC Dashboard