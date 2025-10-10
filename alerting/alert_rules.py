"""
Alert Rules
Predefined alert rule definitions
"""

import logging

logger = logging.getLogger(__name__)


# Predefined alert rules
ALERT_RULES = {
    'high_cpu': {
        'metric': 'cpu_usage_percent',
        'condition': 'greater_than',
        'threshold': 80,
        'severity': 'warning',
        'message': 'CPU usage is high'
    },
    'critical_cpu': {
        'metric': 'cpu_usage_percent',
        'condition': 'greater_than',
        'threshold': 95,
        'severity': 'critical',
        'message': 'CPU usage is critical'
    },
    'high_memory': {
        'metric': 'memory_usage_percent',
        'condition': 'greater_than',
        'threshold': 85,
        'severity': 'warning',
        'message': 'Memory usage is high'
    },
    'high_error_rate': {
        'metric': 'error_rate_percent',
        'condition': 'greater_than',
        'threshold': 5,
        'severity': 'critical',
        'message': 'Error rate is too high'
    },
    'slow_response': {
        'metric': 'avg_response_time',
        'condition': 'greater_than',
        'threshold': 1.0,
        'severity': 'warning',
        'message': 'Response time is slow'
    },
    'low_disk_space': {
        'metric': 'disk_usage_percent',
        'condition': 'greater_than',
        'threshold': 90,
        'severity': 'critical',
        'message': 'Disk space is low'
    }
}


def get_default_rules():
    """
    Get default alert rules
    
    Returns:
        Dictionary of alert rules
    """
    return ALERT_RULES.copy()


def create_custom_rule(name, metric, condition, threshold, severity='warning', message=None):
    """
    Create a custom alert rule
    
    Args:
        name: Rule name
        metric: Metric to monitor
        condition: Condition type
        threshold: Threshold value
        severity: Alert severity
        message: Alert message
        
    Returns:
        Alert rule dictionary
    """
    return {
        'metric': metric,
        'condition': condition,
        'threshold': threshold,
        'severity': severity,
        'message': message or f'{metric} {condition} {threshold}'
    }
