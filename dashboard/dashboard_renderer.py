"""
Dashboard Renderer
Renders dashboard in text format
"""

import logging

logger = logging.getLogger(__name__)


class DashboardRenderer:
    """
    Renders dashboard data in text format
    """
    
    def __init__(self):
        """Initialize dashboard renderer"""
        logger.info("Dashboard Renderer initialized")
    
    def render(self, dashboard_data):
        """
        Render dashboard data
        
        Args:
            dashboard_data: Dashboard data dictionary
            
        Returns:
            Rendered dashboard string
        """
        output = []
        
        output.append("=" * 70)
        output.append("  OBSERVABILITY DASHBOARD")
        output.append("=" * 70)
        
        # Health status
        health = dashboard_data['health_status']
        health_icon = self._get_health_icon(health)
        output.append(f"\n{health_icon} Overall Health: {health.upper()}")
        
        # System metrics
        output.append("\n[EMOJI] System Metrics:")
        metrics = dashboard_data['system_metrics']
        output.append(f"   CPU Usage: {metrics.get('cpu_usage_percent', 0):.1f}%")
        output.append(f"   Memory Usage: {metrics.get('memory_usage_percent', 0):.1f}%")
        output.append(f"   Disk Usage: {metrics.get('disk_usage_percent', 0):.1f}%")
        
        # Active alerts
        output.append(f"\n[EMOJI] Active Alerts: {dashboard_data['alert_count']}")
        for alert in dashboard_data['active_alerts'][:5]:
            output.append(f"   - [{alert['severity'].upper()}] {alert['message']}")
        
        # Recent errors
        output.append(f"\n[EMOJI] Recent Errors: {dashboard_data['error_count']}")
        for log in dashboard_data['recent_errors'][:3]:
            output.append(f"   - {log['message'][:60]}")
        
        # SLA status
        output.append(f"\n[EMOJI] SLA Status:")
        for sla_name, sla_data in dashboard_data['sla_status'].items():
            status_icon = "[EMOJI]" if sla_data.get('compliant', False) else "[EMOJI]"
            output.append(f"   {status_icon} {sla_name}: {sla_data.get('current', 0):.2f}% (target: {sla_data.get('target', 0):.2f}%)")
        
        output.append("\n" + "=" * 70)
        
        return "\n".join(output)
    
    def _get_health_icon(self, health):
        """Get icon for health status"""
        icons = {
            'healthy': '[EMOJI]',
            'warning': '[EMOJI]️',
            'degraded': '[EMOJI]',
            'critical': '[EMOJI]'
        }
        return icons.get(health, '[EMOJI]')
