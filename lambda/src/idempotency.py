"""Idempotency module using DynamoDB conditional writes."""

import os
import logging
from datetime import datetime, timezone
from typing import Tuple, Optional

import boto3
from botocore.exceptions import ClientError
from botocore.config import Config

from src.config import REGION, DDB_TABLE, TTL_SECONDS, RETRY_CONFIG

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize DynamoDB client
ddb = boto3.resource('dynamodb', region_name=REGION, config=RETRY_CONFIG)
table = ddb.Table(DDB_TABLE)


def claim_incident(incident_id: str) -> Tuple[bool, Optional[Exception]]:
    """
    Attempt to claim an incident for remediation.
    
    Uses DynamoDB conditional write to ensure idempotency:
    - If incident_id doesn't exist: create record, return (False, None)
    - If incident_id exists: return (True, None)
    - On error: return (False, error)
    
    Args:
        incident_id: Unique identifier from Sentinel incident
    
    Returns:
        Tuple of (already_claimed, error)
        - already_claimed: True if already remediated, False otherwise
        - error: Exception if operation failed, None otherwise
    """
    try:
        now = datetime.now(timezone.utc)
        ttl = int(now.timestamp()) + TTL_SECONDS
        
        table.put_item(
            Item={
                'incident_id': incident_id,
                'claimed_at': now.isoformat(),
                'ttl': ttl
            },
            ConditionExpression='attribute_not_exists(incident_id)'
        )
        logger.info(f'Claimed incident {incident_id}')
        return False, None
        
    except ddb.meta.client.exceptions.ConditionalCheckFailedException:
        logger.info(f'Incident {incident_id} already claimed')
        return True, None
        
    except ClientError as e:
        logger.error(f'DynamoDB error claiming incident {incident_id}: {e}')
        return False, e