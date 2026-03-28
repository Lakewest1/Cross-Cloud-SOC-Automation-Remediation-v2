"""
sentinel-iam-remediation v3.0 - Production Grade
Cross-cloud SOC auto-remediation: Azure Sentinel → AWS Lambda → IAM
Sir Lakewest Cybersecurity Academy

This Lambda function is triggered by API Gateway when Azure Sentinel detects
a privilege escalation incident. It performs:
1. Input validation and authorization
2. Idempotency check via DynamoDB
3. IAM access key disablement (if severity High/Critical)
4. Email alert via Amazon SES
5. Audit logging to CloudWatch
"""

import json
import logging
import os
from datetime import datetime, timezone
from typing import Dict, Any, Tuple

import boto3
from botocore.exceptions import ClientError
from botocore.config import Config

from src.config import (
    REGION, ACCOUNT_ID, FROM_EMAIL, TO_EMAILS, DDB_TABLE,
    AUTO_REMED, ALLOWED_ARNS, RETRY_CONFIG
)
from src.idempotency import claim_incident
from src.remediation import disable_iam_keys
from src.utils import metric, resp, logger

# Initialize AWS clients with retry configuration
iam = boto3.client('iam', region_name=REGION, config=RETRY_CONFIG)
ses = boto3.client('ses', region_name=REGION, config=RETRY_CONFIG)
cw = boto3.client('cloudwatch', region_name=REGION, config=RETRY_CONFIG)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Main Lambda entry point for Sentinel IAM remediation.
    
    Args:
        event: API Gateway event with incident details
        context: Lambda context object
    
    Returns:
        API Gateway response with remediation status
    """
    logger.info(json.dumps({
        'event': 'INVOKED',
        'id': context.aws_request_id,
        'timestamp': datetime.now(timezone.utc).isoformat()
    }))
    
    # Circuit breaker: check if auto-remediation is enabled
    if AUTO_REMED != 'true':
        logger.info('Auto-remediation disabled by circuit breaker')
        return resp(200, {
            'status': 'DISABLED',
            'message': 'Auto-remediation disabled (AUTO_REMEDIATION=false)'
        })
    
    # Authorization: verify caller ARN
    caller_arn = event.get('requestContext', {}).get('identity', {}).get('userArn', 'unknown')
    if ALLOWED_ARNS and caller_arn not in ALLOWED_ARNS:
        logger.warning(f'Unauthorized caller: {caller_arn}')
        metric('UnauthorizedAccess', 1)
        return resp(403, {'error': 'Unauthorized caller'})
    
    # Parse request body
    try:
        body = json.loads(event['body']) if isinstance(event.get('body'), str) else event.get('body', {})
    except (json.JSONDecodeError, TypeError) as e:
        logger.error(f'Invalid JSON: {e}')
        return resp(400, {'error': 'Invalid JSON in request body'})
    
    # Validate required fields
    incident_id = body.get('incident_id', '').strip()
    if not incident_id:
        logger.error('Missing incident_id')
        return resp(400, {'error': 'Missing incident_id'})
    
    username = body.get('username', '').strip()
    severity = body.get('severity', '').lower()
    
    # Idempotency check
    claimed, err = claim_incident(incident_id)
    if err:
        logger.error(f'Idempotency check failed: {err}')
        metric('RemediationErrors', 1)
        return resp(500, {'error': 'Idempotency check failed'})
    
    if claimed:
        logger.info(f'Incident {incident_id} already remediated')
        return resp(200, {'status': 'ALREADY_REMEDIATED', 'incident_id': incident_id})
    
    # Perform remediation based on severity
    remediation_results = []
    if severity in ('high', 'critical') and username:
        try:
            disabled_keys = disable_iam_keys(username)
            if disabled_keys:
                remediation_results.extend(disabled_keys)
                logger.info(f'Disabled {len(disabled_keys)} keys for {username}')
                metric('RemediationExecuted', len(disabled_keys))
        except Exception as e:
            logger.error(f'Remediation failed for {username}: {e}')
            metric('RemediationErrors', 1)
            remediation_results.append(f'Error: {str(e)}')
    else:
        logger.info(f'Severity {severity} below threshold, no remediation')
    
    # Send email alert
    if FROM_EMAIL and TO_EMAILS:
        try:
            email_body = _build_email_body(incident_id, username, severity, remediation_results)
            ses.send_email(
                Source=FROM_EMAIL,
                Destination={'ToAddresses': TO_EMAILS},
                Message={
                    'Subject': {'Data': f'Sentinel Remediation Alert - {incident_id}'},
                    'Body': {'Html': {'Data': email_body}}
                }
            )
            logger.info(f'Email sent to {", ".join(TO_EMAILS)}')
        except Exception as e:
            logger.error(f'Email send failed: {e}')
            metric('RemediationErrors', 1)
    
    return resp(200, {
        'status': 'COMPLETED',
        'incident_id': incident_id,
        'actions': remediation_results,
        'severity': severity
    })


def _build_email_body(incident_id: str, username: str, severity: str, actions: list) -> str:
    """Build HTML email body for alert."""
    actions_html = ''.join([f'<li>{action}</li>' for action in actions]) if actions else '<li>No remediation actions taken (severity below threshold)</li>'
    
    return f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #d9534f; color: white; padding: 10px; text-align: center; }}
            .content {{ padding: 20px; border: 1px solid #ddd; }}
            .footer {{ font-size: 12px; color: #888; text-align: center; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>🚨 Sentinel Auto-Remediation Alert</h2>
            </div>
            <div class="content">
                <p><strong>Incident ID:</strong> {incident_id}</p>
                <p><strong>Username:</strong> {username}</p>
                <p><strong>Severity:</strong> {severity.upper()}</p>
                <p><strong>Remediation Actions:</strong></p>
                <ul>{actions_html}</ul>
                <p><strong>Timestamp:</strong> {datetime.now(timezone.utc).isoformat()}</p>
            </div>
            <div class="footer">
                <p>Cross-Cloud SOC Auto-Remediation System | Azure Sentinel → AWS Lambda</p>
                <p>This is an automated alert. Please do not reply.</p>
            </div>
        </div>
    </body>
    </html>
    """