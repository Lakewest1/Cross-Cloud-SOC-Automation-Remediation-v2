"""Utility functions for logging, metrics, and responses."""

import json
import logging
from typing import Any, Dict

import boto3
from botocore.config import Config

from src.config import REGION, RETRY_CONFIG

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize CloudWatch client
cw = boto3.client('cloudwatch', region_name=REGION, config=RETRY_CONFIG)


def metric(metric_name: str, value: float, unit: str = 'Count') -> None:
    """
    Send custom metric to CloudWatch.
    
    Args:
        metric_name: Name of the metric (e.g., 'RemediationExecuted')
        value: Metric value
        unit: Unit type ('Count', 'Seconds', 'Percent', etc.)
    """
    try:
        cw.put_metric_data(
            Namespace='SentinelRemediation',
            MetricData=[
                {
                    'MetricName': metric_name,
                    'Value': value,
                    'Unit': unit,
                    'Timestamp': 'now'
                }
            ]
        )
    except Exception as e:
        logger.error(f'Failed to send metric {metric_name}: {e}')


def resp(status_code: int, body: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create API Gateway response object.
    
    Args:
        status_code: HTTP status code
        body: Response body dictionary
    
    Returns:
        API Gateway response object
    """
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body)
    }