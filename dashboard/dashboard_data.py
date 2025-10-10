"""
Dashboard Data
Provides data for performance dashboard
"""

import logging

logger = logging.getLogger(__name__)


class DashboardData:
    """
    Dashboard data provider
    """
    
    def __init__(self, metrics_collector, alert_manager, log_aggregator, sla_monitor):
        """
        Initialize dashboard data provider
        
        Args:
            metrics_collector: MetricsCollector instance
            alert_manager: AlertManager instance
            log_aggregator: LogAggregator instance
            sla_monitor: SLAMonitor instance
        """
        self.metrics_collector = metrics_collector
        self.alert_manager = alert_manager
        self.log_aggregator = log_aggregator
        self.sla_monitor = sla_monitor
        
        logger.info("Dashboard Data initialized")
    
    def get_dashboard_data(self):
        """
        Get complete dashboard data
        
        Returns:
            Dashboard data dictionary
        """
        # Collect current system metrics
        system_metrics = self.metrics_collector.collect_system_metrics()
        
        # Get active alerts
        active_alerts = self.alert_manager.get_active_alerts()
        
        # Get recent logs
        error_logs = self.log_aggregator.get_logs(level='ERROR', hours=1, limit=10)
        
        # Get SLA status
        sla_status = self.sla_monitor.get_all_sla_status()
        
        # Determine overall health
        health_status = self._calculate_health_status(system_metrics, active_alerts)
        
        return {
            'health_status': health_status,
            'system_metrics': system_metrics,
            'active_alerts': active_alerts,
            'alert_count': len(active_alerts),
            'recent_errors': error_logs,
            'error_count': len(error_logs),
            'sla_status': sla_status,
            'timestamp': time.time()
        }
    
    def _calculate_health_status(self, metrics, alerts):
        """
        Calculate overall health status
        
        Args:
            metrics: System metrics
            alerts: Active alerts
            
        Returns:
            Health status string
        """
        # Check for critical alerts
        critical_alerts = [a for a in alerts if a.get('severity') == 'critical']
        
        if critical_alerts:
            return 'critical'
        
        # Check for warnings
        if alerts:
            return 'warning'
        
        # Check system metrics
        if metrics.get('cpu_usage_percent', 0) > 90:
            return 'degraded'
        
        if metrics.get('memory_usage_percent', 0) > 90:
            return 'degraded'
        
        return 'healthy'
    
    def get_metrics_summary(self):
        """Get summary of all metrics"""
        all_metrics = self.metrics_collector.get_all_metrics()
        
        summary = {}
        for metric_name in all_metrics:
            latest = self.metrics_collector.get_latest_value(metric_name)
            avg = self.metrics_collector.get_average(metric_name, window_seconds=300)
            
            summary[metric_name] = {
                'latest': latest,
                'avg_5min': avg
            }
        
        return summary


import time
