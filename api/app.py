"""
Flask API with Observability
Provides REST API for observability platform
"""

from flask import Flask, request, jsonify
import logging
import os

from metrics.metrics_collector import MetricsCollector
from metrics.metrics_store import MetricsStore
from alerting.alert_manager import AlertManager
from alerting.alert_rules import get_default_rules
from alerting.alert_store import AlertStore
from logging.log_aggregator import LogAggregator
from dashboard.dashboard_data import DashboardData
from dashboard.dashboard_renderer import DashboardRenderer
from sla.sla_monitor import SLAMonitor
from incident.incident_detector import IncidentDetector
from incident.incident_responder import IncidentResponder
from incident.incident_store import IncidentStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize components
db_path = os.getenv('DATABASE_PATH', 'observability.db')
metrics_collector = MetricsCollector()
metrics_store = MetricsStore(db_path)
alert_manager = AlertManager()
alert_store = AlertStore(db_path)
log_aggregator = LogAggregator(db_path)
sla_monitor = SLAMonitor(db_path)
incident_detector = IncidentDetector()
incident_responder = IncidentResponder()
incident_store = IncidentStore(db_path)

# Setup default alert rules
default_rules = get_default_rules()
for rule_name, rule_config in default_rules.items():
    alert_manager.add_rule(rule_name, **rule_config)

# Setup default SLAs
sla_monitor.define_sla('api_uptime', target=99.9, metric_type='uptime')
sla_monitor.define_sla('error_rate', target=99.0, metric_type='error_rate')

# Setup incident response playbooks
incident_responder.add_playbook('high_cpu', ['log_incident', 'send_alert'])
incident_responder.add_playbook('high_error_rate', ['log_incident', 'send_alert', 'restart_service'])
incident_responder.add_playbook('service_down', ['log_incident', 'send_alert', 'restart_service', 'notify_team'])

# Dashboard
dashboard_data = DashboardData(metrics_collector, alert_manager, log_aggregator, sla_monitor)
dashboard_renderer = DashboardRenderer()


@app.route('/')
def index():
    """Root endpoint"""
    return jsonify({
        'message': 'Local Observability Platform',
        'version': '1.0.0',
        'features': [
            'Metrics Collection',
            'Alerting System',
            'Log Aggregation',
            'Performance Dashboard',
            'SLA Monitoring',
            'Incident Response'
        ]
    })


@app.route('/health')
def health():
    """Health check"""
    return jsonify({'status': 'healthy'})


@app.route('/api/metrics/collect', methods=['POST'])
def collect_metric():
    """Collect a custom metric"""
    data = request.get_json()
    
    if not data or 'name' not in data or 'value' not in data:
        return jsonify({'error': 'name and value required'}), 400
    
    metrics_collector.collect_metric(data['name'], data['value'], data.get('labels'))
    metrics_store.save_metric(data['name'], data['value'], data.get('labels'))
    
    return jsonify({'status': 'success', 'message': 'Metric collected'})


@app.route('/api/metrics/<metric_name>', methods=['GET'])
def get_metric(metric_name):
    """Get metric values"""
    values = metrics_collector.get_metric(metric_name, limit=100)
    
    return jsonify({
        'metric': metric_name,
        'values': values,
        'count': len(values)
    })


@app.route('/api/metrics/system', methods=['GET'])
def get_system_metrics():
    """Get current system metrics"""
    metrics = metrics_collector.collect_system_metrics()
    
    return jsonify(metrics)


@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Get active alerts"""
    alerts = alert_manager.get_active_alerts()
    
    return jsonify({
        'alerts': alerts,
        'count': len(alerts)
    })


@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Get logs"""
    level = request.args.get('level')
    hours = int(request.args.get('hours', 24))
    
    logs = log_aggregator.get_logs(level=level, hours=hours, limit=100)
    
    return jsonify({
        'logs': logs,
        'count': len(logs)
    })


@app.route('/api/logs/add', methods=['POST'])
def add_log():
    """Add a log entry"""
    data = request.get_json()
    
    if not data or 'level' not in data or 'message' not in data:
        return jsonify({'error': 'level and message required'}), 400
    
    log_aggregator.log(data['level'], data['message'], data.get('source'))
    
    return jsonify({'status': 'success', 'message': 'Log recorded'})


@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    """Get dashboard data"""
    # Collect current metrics
    metrics_collector.collect_system_metrics()
    
    # Evaluate alerts
    alert_manager.evaluate_all_rules(metrics_collector)
    
    # Get dashboard data
    data = dashboard_data.get_dashboard_data()
    
    return jsonify(data)


@app.route('/api/dashboard/render', methods=['GET'])
def render_dashboard():
    """Get rendered dashboard"""
    data = dashboard_data.get_dashboard_data()
    rendered = dashboard_renderer.render(data)
    
    return rendered, 200, {'Content-Type': 'text/plain'}


@app.route('/api/sla', methods=['GET'])
def get_sla_status():
    """Get SLA status"""
    status = sla_monitor.get_all_sla_status()
    
    return jsonify(status)


@app.route('/api/incidents', methods=['GET'])
def get_incidents():
    """Get recent incidents"""
    incidents = incident_store.get_recent_incidents(hours=24)
    
    return jsonify({
        'incidents': incidents,
        'count': len(incidents)
    })


if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    print("=" * 60)
    print("Local Observability Platform - Flask API")
    print("=" * 60)
    print(f"Starting on port {port}")
    print("Features:")
    print("  - Metrics Collection")
    print("  - Alerting System")
    print("  - Log Aggregation")
    print("  - Performance Dashboard")
    print("  - SLA Monitoring")
    print("  - Incident Response")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
