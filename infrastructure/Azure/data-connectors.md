
---

## 📁 infrastructure/azure/data-connectors.md

```markdown
# Azure Sentinel Data Connectors Configuration

## Overview

This document details the configuration of all data connectors required for the Cross-Cloud SOC Auto-Remediation System.

## Connector Summary

| Connector | Purpose | Status |
|-----------|---------|--------|
| Azure Activity | Azure control plane logs | ✅ Configured |
| Microsoft Entra ID | Identity and sign-in logs | ✅ Configured |
| AWS CloudTrail (OIDC) | AWS API activity logs | ✅ Configured |

---

## 1. Azure Activity Connector

### Prerequisites
- Azure subscription with Owner role
- Log Analytics workspace created
- Microsoft Sentinel enabled

### Configuration Steps

**Portal Method:**

1. Navigate to **Microsoft Sentinel** → **Data connectors**
2. Search for "Azure Activity"
3. Click **Open connector page**

4. **Configure Diagnostic Settings:**
   - Click **Launch Azure Policy Assignment**
   - Scope: Select your subscription
   - Policy definition: "Configure Azure Activity logs to stream to specified Log Analytics workspace"
   - Primary workspace: soclawlab
   - Remediation: ✅ Checked
   - Managed identity: Select your SOC-lab identity
   - Click **Review + Create**

5. **Verify Connection:**
   - Status should show "Connected"
   - Last log received: Recent timestamp

**ARM Template Deployment:**

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "workspaceName": {
      "type": "string",
      "defaultValue": "soclawlab"
    },
    "subscriptionId": {
      "type": "string"
    }
  },
  "resources": [
    {
      "type": "Microsoft.Resources/deployments",
      "apiVersion": "2021-04-01",
      "name": "azureActivityConnector",
      "properties": {
        "mode": "Incremental",
        "template": {
          "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
          "contentVersion": "1.0.0.0",
          "resources": [
            {
              "type": "Microsoft.Insights/diagnosticSettings",
              "apiVersion": "2021-05-01-preview",
              "name": "AzureActivityLogsToSentinel",
              "scope": "/subscriptions/[parameters('subscriptionId')]",
              "properties": {
                "workspaceId": "[resourceId('Microsoft.OperationalInsights/workspaces', parameters('workspaceName'))]",
                "logs": [
                  {
                    "category": "Administrative",
                    "enabled": true
                  },
                  {
                    "category": "Security",
                    "enabled": true
                  },
                  {
                    "category": "ServiceHealth",
                    "enabled": true
                  },
                  {
                    "category": "Alert",
                    "enabled": true
                  },
                  {
                    "category": "Recommendation",
                    "enabled": true
                  },
                  {
                    "category": "Policy",
                    "enabled": true
                  },
                  {
                    "category": "Autoscale",
                    "enabled": true
                  },
                  {
                    "category": "ResourceHealth",
                    "enabled": true
                  }
                ]
              }
            }
          ]
        }
      }
    }
  ]
}