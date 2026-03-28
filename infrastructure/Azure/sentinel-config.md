# Microsoft Sentinel Configuration Guide

## Overview

This guide documents the complete configuration of Microsoft Sentinel for the Cross-Cloud SOC Auto-Remediation System.

## Prerequisites

- Azure Subscription with Owner or Contributor access
- Log Analytics Workspace created
- Microsoft Sentinel enabled

---

## 1. Log Analytics Workspace Setup

### Step 1: Create Log Analytics Workspace

```bash
# Azure CLI commands
az login

# Create resource group
az group create \
  --name SOC-lab-01 \
  --location eastus

# Create Log Analytics workspace
az monitor log-analytics workspace create \
  --resource-group SOC-lab-01 \
  --workspace-name soclawlab \
  --location eastus \
  --sku PerGB2018

Portal Method:

Navigate to Azure Portal → Log Analytics workspaces

Click + Create

Configure:

Subscription: Your subscription

Resource Group: SOC-lab-01

Name: soclawlab (must be unique)

Region: East US

Click Review + Create → Create

##STEP 2 : 
# Enable Sentinel on workspace
az sentinel workspace-manager member create \
  --resource-group SOC-lab-01 \
  --workspace-name soclawlab \
  --member-workspace-id $(az monitor log-analytics workspace show \
    --resource-group SOC-lab-01 \
    --workspace-name soclawlab \
    --query customerId -o tsv)
Portal Method:

Search "Microsoft Sentinel"

Click + Create

Select workspace soclawlab

Click Add

Wait 30-60 seconds for initialization

##STEP 3 : 
Data Connectors Configuration
Azure Activity Logs
Portal Method:

Sentinel → Data connectors

Search "Azure Activity"

Click Open connector page

Configure diagnostic settings:

Select subscription

Click Launch Azure Policy Assignment

Scope: Select subscription

Policy definition: "Configure Azure Activity logs to stream to specified Log Analytics workspace"

Primary workspace: soclawlab

Remediation: Checked

Managed identity: Select SOC-lab identity

Click Review + Create

##STEP 4 : VERIFY LOGS FLOW
AzureActivity
| where TimeGenerated > ago(24h)
| take 10

Microsoft Entra ID (Azure AD) Logs
Portal Method:

Navigate to Microsoft Entra ID

Diagnostic settings → + Add diagnostic setting

Name: Entra-ID-Logs-To-Sentinel

Categories:

✅ AuditLogs

✅ SignInLogs

✅ ServicePrincipalSignInLogs

Destination: Send to Log Analytics workspace → soclawlab

Click Save

Wait 3-5 minutes for initial ingestion

Verify:

SigninLogs
| where TimeGenerated > ago(24h)
| take 10

AuditLogs
| where TimeGenerated > ago(24h)
| take 10

AWS CloudTrail (OIDC Connector)
Prerequisites:

AWS account with CloudTrail enabled

OIDC identity provider configured in AWS

Portal Method:

Sentinel → Data connectors

Search "Amazon Web Services"

Click Open connector page

Configure OIDC authentication:

Click Launch OIDC Configuration Script

Run PowerShell script to create AWS IAM role

Copy the OIDC token URL

In AWS Console:

IAM → Identity providers → Create provider

Provider type: OpenID Connect

Provider URL: (from Azure)

Audience: api://AzureADTokenExchange

Create IAM role with CloudTrail read permissions

Back in Azure:

Paste role ARN

Click Connect

Verify:

kql
AWSCloudTrail
| where TimeGenerated > ago(24h)
| take 10