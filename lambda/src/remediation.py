"""IAM remediation actions with least privilege enforcement."""

import logging
from typing import List

import boto3
from botocore.exceptions import ClientError
from botocore.config import Config

from src.config import REGION, RETRY_CONFIG

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize IAM client
iam = boto3.client('iam', region_name=REGION, config=RETRY_CONFIG)


def disable_iam_keys(username: str) -> List[str]:
    """
    Disable all active IAM access keys for a user.
    
    Requires IAM policy with tag condition:
    - iam:ResourceTag/ManagedBy == "Sentinel"
    
    Args:
        username: IAM username to remediate
    
    Returns:
        List of disabled key IDs
    
    Raises:
        ClientError: If IAM API calls fail
    """
    disabled_keys = []
    
    try:
        # List all access keys for the user
        response = iam.list_access_keys(UserName=username)
        keys = response.get('AccessKeyMetadata', [])
        
        for key in keys:
            if key['Status'] == 'Active':
                try:
                    iam.update_access_key(
                        UserName=username,
                        AccessKeyId=key['AccessKeyId'],
                        Status='Inactive'
                    )
                    disabled_keys.append(key['AccessKeyId'])
                    logger.info(f'Disabled key {key["AccessKeyId"]} for {username}')
                except ClientError as e:
                    logger.error(f'Failed to disable key {key["AccessKeyId"]}: {e}')
                    raise
        
        if not disabled_keys:
            logger.info(f'No active keys found for {username}')
            
    except ClientError as e:
        logger.error(f'Failed to list keys for {username}: {e}')
        raise
    
    return disabled_keys


def revoke_user_sessions(username: str) -> bool:
    """
    Revoke all active sessions for a user (requires additional permissions).
    
    This is a placeholder for future enhancement. Full implementation
    would require organizations API or user session management.
    
    Args:
        username: IAM username to revoke sessions for
    
    Returns:
        True if successful, False otherwise
    """
    # Note: IAM does not have a direct "revoke all sessions" API.
    # To fully revoke access, combine key disable with:
    # - Detach all policies
    # - Delete login profile
    # - Change password
    
    logger.info(f'Revoke sessions for {username} - requires additional permissions')
    return False