"""
Local Observability Platform - Main Demonstration
Shows examples of all observability features
"""

import os
import time
from metrics.metrics_collector import MetricsCollector
from metrics.metrics_aggregator import MetricsAggregator
from alerting.alert_manager import AlertManager
from alerting.alert_rules import get_default_rules
from logging.log_aggregator import LogAggregator
from dashboard.dashboard_data import DashboardData
from dashboard.dashboard_renderer import DashboardRenderer
from sla.sla_monitor import SLAMonitor
from incident.incident_detector import IncidentDetector
from incident.incident_responder import IncidentResponder


def print_section(title):
    """Print section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def demo_metrics_collection():
    """Demonstrate metrics collection"""
    print_section("1. Metrics Collection")
    
    collector = MetricsCollector()
    
    # Collect system metrics
    print("\n📊 Collecting system metrics:")
    system_metrics = collector.collect_system_metrics()
    
    print(f"   CPU Usage: {system_metrics['cpu_usage_percent']:.1f}%")
    print(f"   Memory Usage: {system_metrics['memory_usage_percent']:.1f}%")
    print(f"   Disk Usage: {system_metrics['disk_usage_percent']:.1f}%")
    
    # Collect custom metrics
    print("\n📈 Collecting custom metrics:")
    collector.collect_metric('http_requests', 150)
    collector.collect_metric('response_time', 0.05)
    collector.collect_metric('error_count', 3)
    
    print("   ✅ 3 custom metrics collected")
    
    # Get stats
    stats = collector.get_stats()
    print(f"\n📊 Collector Stats:")
    print(f"   Tracked metrics: {stats['tracked_metrics']}")
    print(f"   Total data points: {stats['total_data_points']}")


def demo_alerting():
    """Demonstrate alerting system"""
    print_section("2. Alerting System")
    
    alert_manager = AlertManager()
    collector = MetricsCollector()
    
    # Add alert rules
    print("\n🚨 Adding alert rules:")
    alert_manager.add_rule(
        name='high_cpu',
        metric='cpu_usage',
        condition='greater_than',
        threshold=80,
        severity='warning'
    )
    print("   ✅ Rule added: high_cpu (threshold: 80%)")
    
    # Simulate high CPU
    print("\n📊 Simulating high CPU usage:")
    collector.collect_metric('cpu_usage', 85)
    
    # Evaluate rules
    fired = alert_manager.evaluate_all_rules(collector)
    
    if fired:
        print(f"   🚨 Alerts fired: {fired}")
    
    # Get active alerts
    active = alert_manager.get_active_alerts()
    print(f"\n📋 Active alerts: {len(active)}")


def demo_log_aggregation():
    """Demonstrate log aggregation"""
    print_section("3. Log Aggregation")
    
    # Clean up old database
    db_path = 'demo.db'
    if os.path.exists(db_path):
        os.remove(db_path)
    
    log_agg = LogAggregator(db_path)
    
    # Log messages
    print("\n📝 Logging messages:")
    log_agg.log('INFO', 'Application started')
    log_agg.log('INFO', 'User logged in')
    log_agg.log('WARNING', 'High memory usage detected')
    log_agg.log('ERROR', 'Database connection failed')
    log_agg.log('CRITICAL', 'Service unavailable')
    
    print("   ✅ 5 log entries recorded")
    
    # Get logs by level
    print("\n📋 Error logs:")
    errors = log_agg.get_logs(level='ERROR', hours=24)
    
    for log in errors:
        print(f"   - [{log['level']}] {log['message']}")
    
    # Get log counts
    counts = log_agg.get_log_count_by_level()
    print(f"\n📊 Log counts by level:")
    for level, count in counts.items():
        print(f"   {level}: {count}")


def demo_sla_monitoring():
    """Demonstrate SLA monitoring"""
    print_section("4. SLA Monitoring")
    
    db_path = 'demo.db'
    sla_monitor = SLAMonitor(db_path)
    
    # Define SLA
    print("\n📋 Defining SLA:")
    sla_monitor.define_sla('api_uptime', target=99.9, metric_type='uptime')
    print("   ✅ SLA defined: api_uptime (target: 99.9%)")
    
    # Record SLA metrics
    print("\n📊 Recording SLA metrics:")
    sla_monitor.record_sla_metric('api_uptime', 99.95)
    sla_monitor.record_sla_metric('api_uptime', 99.92)
    sla_monitor.record_sla_metric('api_uptime', 99.98)
    
    print("   ✅ 3 measurements recorded")
    
    # Get SLA status
    status = sla_monitor.get_sla_status('api_uptime')
    
    print(f"\n📈 SLA Status:")
    print(f"   Current: {status['current']:.2f}%")
    print(f"   Target: {status['target']:.2f}%")
    print(f"   Compliant: {'✅ Yes' if status['compliant'] else '❌ No'}")


def demo_incident_response():
    """Demonstrate incident response"""
    print_section("5. Automated Incident Response")
    
    responder = IncidentResponder()
    
    # Add playbook
    print("\n📋 Adding incident response playbook:")
    responder.add_playbook('high_error_rate', [
        'log_incident',
        'send_alert',
        'restart_service'
    ])
    
    print("   ✅ Playbook added for high_error_rate")
    
    # Trigger response
    print("\n🚨 Triggering incident response:")
    actions = responder.respond('high_error_rate', context={'error_rate': 15.5})
    
    print(f"\n✅ Actions executed: {len(actions)}")
    for action in actions:
        status = "✅" if action['success'] else "❌"
        print(f"   {status} {action['action']}")


def demo_dashboard():
    """Demonstrate performance dashboard"""
    print_section("6. Performance Dashboard")
    
    db_path = 'demo.db'
    
    # Initialize components
    collector = MetricsCollector()
    alert_mgr = AlertManager()
    log_agg = LogAggregator(db_path)
    sla_mon = SLAMonitor(db_path)
    
    # Setup
    sla_mon.define_sla('uptime', target=99.9)
    alert_mgr.add_rule('test_alert', 'cpu_usage', 'greater_than', 50, 'warning')
    
    # Collect some data
    collector.collect_metric('cpu_usage', 45)
    log_agg.log('INFO', 'Test log entry')
    sla_mon.record_sla_metric('uptime', 99.95)
    
    # Get dashboard data
    dashboard = DashboardData(collector, alert_mgr, log_agg, sla_mon)
    renderer = DashboardRenderer()
    
    data = dashboard.get_dashboard_data()
    rendered = renderer.render(data)
    
    print("\n" + rendered)


def demo_metrics_aggregation():
    """Demonstrate metrics aggregation"""
    print_section("7. Metrics Aggregation")
    
    aggregator = MetricsAggregator()
    
    # Sample metrics
    metrics = [
        {'value': 10, 'timestamp': time.time()},
        {'value': 20, 'timestamp': time.time()},
        {'value': 30, 'timestamp': time.time()},
        {'value': 40, 'timestamp': time.time()}
    ]
    
    print("\n📊 Aggregating metrics:")
    print(f"   Values: {[m['value'] for m in metrics]}")
    
    # Calculate aggregations
    results = aggregator.aggregate_all(metrics)
    
    print(f"\n📈 Aggregation Results:")
    print(f"   Count: {results['count']}")
    print(f"   Sum: {results['sum']}")
    print(f"   Avg: {results['avg']:.2f}")
    print(f"   Min: {results['min']}")
    print(f"   Max: {results['max']}")


def main():
    """Run all demonstrations"""
    print("\n" + "=" * 70)
    print("  Local Observability Platform - Demonstration")
    print("=" * 70)
    
    try:
        demo_metrics_collection()
        demo_alerting()
        demo_log_aggregation()
        demo_sla_monitoring()
        demo_incident_response()
        demo_dashboard()
        demo_metrics_aggregation()
        
        print("\n" + "=" * 70)
        print("  All Demonstrations Completed!")
        print("=" * 70)
        print("\nKey Features Demonstrated:")
        print("  1. Metrics Collection - System and custom metrics")
        print("  2. Alerting System - Threshold-based alerts")
        print("  3. Log Aggregation - Collect and query logs")
        print("  4. SLA Monitoring - Track service levels")
        print("  5. Incident Response - Automated remediation")
        print("  6. Performance Dashboard - Health overview")
        print("  7. Metrics Aggregation - Statistical analysis")
        print("\nTo run Flask API:")
        print("  python api/app.py")
        print("\nTo run tests:")
        print("  python tests.py")
        print()
        
        # Cleanup
        if os.path.exists('demo.db'):
            os.remove('demo.db')
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
