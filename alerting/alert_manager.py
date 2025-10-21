"""
Alert Manager
Manages alerts and alert rules
"""

import logging
import time

logger = logging.getLogger(__name__)


class AlertManager:
    """
    Alert management system
    """
    
    def __init__(self):
        """Initialize alert manager"""
        self.rules = {}
        self.active_alerts = {}
        self.alert_history = []
        self.cooldown_period = 300  # 5 minutes
        
        logger.info("Alert Manager initialized")
    
    def add_rule(self, name, metric, condition, threshold, severity='warning', message=None):
        """
        Add alert rule
        
        Args:
            name: Rule name
            metric: Metric to monitor
            condition: Condition (greater_than, less_than, equals)
            threshold: Threshold value
            severity: Alert severity (info, warning, critical)
            message: Optional custom message
        """
        self.rules[name] = {
            'metric': metric,
            'condition': condition,
            'threshold': threshold,
            'severity': severity,
            'message': message or f'{metric} {condition} {threshold}'
        }
        
        logger.info(f"Alert rule added: {name}")
    
    def evaluate_rule(self, rule_name, current_value):
        """
        Evaluate alert rule
        
        Args:
            rule_name: Rule name
            current_value: Current metric value
            
        Returns:
            True if alert should fire, False otherwise
        """
        if rule_name not in self.rules:
            return False
        
        rule = self.rules[rule_name]
        condition = rule['condition']
        threshold = rule['threshold']
        
        if condition == 'greater_than':
            return current_value > threshold
        elif condition == 'less_than':
            return current_value < threshold
        elif condition == 'equals':
            return current_value == threshold
        elif condition == 'not_equals':
            return current_value != threshold
        
        return False
    
    def fire_alert(self, rule_name, current_value):
        """
        Fire an alert
        
        Args:
            rule_name: Rule name
            current_value: Current metric value
        """
        # Check cooldown
        if rule_name in self.active_alerts:
            last_fired = self.active_alerts[rule_name]['fired_at']
            if time.time() - last_fired < self.cooldown_period:
                logger.debug(f"Alert {rule_name} in cooldown period")
                return
        
        rule = self.rules[rule_name]
        
        alert = {
            'rule_name': rule_name,
            'metric': rule['metric'],
            'current_value': current_value,
            'threshold': rule['threshold'],
            'severity': rule['severity'],
            'message': rule['message'],
            'fired_at': time.time()
        }
        
        self.active_alerts[rule_name] = alert
        self.alert_history.append(alert)
        
        logger.warning(f"ALERT FIRED: {rule_name} - {rule['message']} (value: {current_value})")
        
        print(f"\n[EMOJI] ALERT: {rule['severity'].upper()}")
        print(f"   Rule: {rule_name}")
        print(f"   Message: {rule['message']}")
        print(f"   Current: {current_value}, Threshold: {rule['threshold']}")
    
    def resolve_alert(self, rule_name):
        """
        Resolve an active alert
        
        Args:
            rule_name: Rule name
        """
        if rule_name in self.active_alerts:
            del self.active_alerts[rule_name]
            logger.info(f"Alert resolved: {rule_name}")
    
    def get_active_alerts(self):
        """Get all active alerts"""
        return list(self.active_alerts.values())
    
    def get_alert_history(self, limit=100):
        """Get alert history"""
        return self.alert_history[-limit:]
    
    def evaluate_all_rules(self, metrics_collector):
        """
        Evaluate all rules against current metrics
        
        Args:
            metrics_collector: MetricsCollector instance
            
        Returns:
            List of fired alerts
        """
        fired_alerts = []
        
        for rule_name, rule in self.rules.items():
            metric_name = rule['metric']
            current_value = metrics_collector.get_latest_value(metric_name)
            
            if current_value is not None:
                if self.evaluate_rule(rule_name, current_value):
                    self.fire_alert(rule_name, current_value)
                    fired_alerts.append(rule_name)
                else:
                    # Resolve if was active
                    if rule_name in self.active_alerts:
                        self.resolve_alert(rule_name)
        
        return fired_alerts
