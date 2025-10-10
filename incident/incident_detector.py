"""
Incident Detector
Detects incidents from metrics and alerts
"""

import logging

logger = logging.getLogger(__name__)


class IncidentDetector:
    """
    Incident detection system
    """
    
    def __init__(self):
        """Initialize incident detector"""
        self.detection_rules = {}
        logger.info("Incident Detector initialized")
    
    def add_detection_rule(self, incident_type, condition_func, description):
        """
        Add incident detection rule
        
        Args:
            incident_type: Type of incident
            condition_func: Function that returns True if incident detected
            description: Incident description
        """
        self.detection_rules[incident_type] = {
            'condition': condition_func,
            'description': description
        }
        
        logger.info(f"Detection rule added: {incident_type}")
    
    def detect_incidents(self, metrics, alerts, logs):
        """
        Detect incidents from current state
        
        Args:
            metrics: Current metrics
            alerts: Active alerts
            logs: Recent logs
            
        Returns:
            List of detected incidents
        """
        incidents = []
        
        for incident_type, rule in self.detection_rules.items():
            try:
                if rule['condition'](metrics, alerts, logs):
                    incident = {
                        'type': incident_type,
                        'description': rule['description'],
                        'detected_at': time.time()
                    }
                    incidents.append(incident)
                    logger.warning(f"Incident detected: {incident_type}")
            except Exception as e:
                logger.error(f"Error detecting {incident_type}: {e}")
        
        return incidents
    
    def detect_high_error_rate(self, error_count, total_requests, threshold=5):
        """
        Detect high error rate
        
        Args:
            error_count: Number of errors
            total_requests: Total requests
            threshold: Error rate threshold percentage
            
        Returns:
            True if incident detected
        """
        if total_requests == 0:
            return False
        
        error_rate = (error_count / total_requests) * 100
        
        return error_rate > threshold
    
    def detect_service_down(self, health_check_failures, threshold=3):
        """
        Detect service down
        
        Args:
            health_check_failures: Number of consecutive failures
            threshold: Failure threshold
            
        Returns:
            True if incident detected
        """
        return health_check_failures >= threshold


import time
