# Local Observability Platform

Educational Python application demonstrating **local observability**, **metrics collection**, **alerting system**, **log aggregation**, **performance dashboard**, **SLA monitoring**, and **automated incident response** with **SQLite3 storage**.

## Features

### 📊 Metrics Collection
- **System Metrics** - CPU, memory, disk usage
- **Application Metrics** - Custom metrics with labels
- **Metric Storage** - SQLite persistence
- **Metric Aggregation** - Sum, avg, min, max, percentiles
- **Historical Data** - Query past metrics

### 🚨 Alerting System
- **Alert Rules** - Threshold-based alerting
- **Alert Evaluation** - Automatic rule checking
- **Alert Firing** - Trigger alerts on violations
- **Alert History** - Store in SQLite
- **Cooldown Period** - Prevent alert spam
- **Multiple Severities** - Info, warning, critical

### 📝 Log Aggregation
- **Log Collection** - Collect application logs
- **Log Levels** - INFO, WARNING, ERROR, CRITICAL
- **Log Storage** - SQLite persistence
- **Log Querying** - Search and filter logs
- **Log Statistics** - Count by level
- **Log Retention** - Auto-delete old logs

### 📈 Performance Dashboard
- **Health Overview** - Overall system health
- **System Metrics** - Real-time system stats
- **Active Alerts** - Current alerts
- **Recent Errors** - Latest error logs
- **SLA Status** - SLA compliance
- **Text Rendering** - ASCII dashboard

### 📋 SLA Monitoring
- **SLA Definitions** - Define service level targets
- **Uptime Tracking** - Track service availability
- **Error Rate Tracking** - Monitor error percentage
- **SLA Compliance** - Check against targets
- **SLA History** - Historical SLA data (SQLite)

### 🔧 Automated Incident Response
- **Incident Detection** - Auto-detect issues
- **Response Playbooks** - Define response actions
- **Automated Actions** - Log, alert, restart, scale
- **Incident History** - Store in SQLite
- **Response Tracking** - Track all responses

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Amruth22/Python-Local-Observability-Platform.git
cd Python-Local-Observability-Platform
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Demonstrations
```bash
python main.py
```

### 5. Run Flask API
```bash
python api/app.py
```

### 6. Run Tests
```bash
python tests.py
```

## Project Structure

```
Python-Local-Observability-Platform/
│
├── metrics/
│   ├── metrics_collector.py     # Metrics collection
│   ├── metrics_store.py         # SQLite storage
│   └── metrics_aggregator.py    # Aggregation
│
├── alerting/
│   ├── alert_manager.py         # Alert management
│   ├── alert_rules.py           # Rule definitions
│   └── alert_store.py           # SQLite storage
│
├── logging/
│   ├── log_aggregator.py        # Log collection
│   ├── log_parser.py            # Log parsing
│   └── log_store.py             # SQLite storage
│
├── dashboard/
│   ├── dashboard_data.py        # Data provider
│   └── dashboard_renderer.py    # Text rendering
│
├── sla/
│   ├── sla_monitor.py           # SLA monitoring
│   └── sla_store.py             # SQLite storage
│
├── incident/
│   ├── incident_detector.py     # Detection
│   ├── incident_responder.py    # Auto-response
│   └── incident_store.py        # SQLite storage
│
├── api/
│   └── app.py                   # Flask API
│
├── main.py                      # Demonstration
├── tests.py                     # 10 unit tests
└── README.md                    # This file
```

## Usage Examples

### Metrics Collection

```python
from metrics.metrics_collector import MetricsCollector

collector = MetricsCollector()

# Collect system metrics
system_metrics = collector.collect_system_metrics()
print(f"CPU: {system_metrics['cpu_usage_percent']}%")

# Collect custom metric
collector.collect_metric('http_requests', 150, labels={'method': 'GET'})

# Get metric
values = collector.get_metric('http_requests')
```

### Alerting

```python
from alerting.alert_manager import AlertManager

alert_manager = AlertManager()

# Add alert rule
alert_manager.add_rule(
    name='high_cpu',
    metric='cpu_usage',
    condition='greater_than',
    threshold=80,
    severity='warning'
)

# Evaluate rules
fired_alerts = alert_manager.evaluate_all_rules(metrics_collector)
```

### Log Aggregation

```python
from logging.log_aggregator import LogAggregator

log_agg = LogAggregator('observability.db')

# Log messages
log_agg.log('INFO', 'Application started')
log_agg.log('ERROR', 'Database connection failed')

# Query logs
errors = log_agg.get_logs(level='ERROR', hours=24)
```

### SLA Monitoring

```python
from sla.sla_monitor import SLAMonitor

sla_monitor = SLAMonitor('observability.db')

# Define SLA
sla_monitor.define_sla('api_uptime', target=99.9)

# Record metric
sla_monitor.record_sla_metric('api_uptime', 99.95)

# Get status
status = sla_monitor.get_sla_status('api_uptime')
print(f"Compliant: {status['compliant']}")
```

### Incident Response

```python
from incident.incident_responder import IncidentResponder

responder = IncidentResponder()

# Add playbook
responder.add_playbook('high_error_rate', [
    'log_incident',
    'send_alert',
    'restart_service'
])

# Respond to incident
actions = responder.respond('high_error_rate', context={'error_rate': 15})
```

## API Endpoints

### Metrics

- `POST /api/metrics/collect` - Collect metric
- `GET /api/metrics/<name>` - Get metric values
- `GET /api/metrics/system` - Get system metrics

### Alerts

- `GET /api/alerts` - Get active alerts

### Logs

- `GET /api/logs` - Get logs (filter by level)
- `POST /api/logs/add` - Add log entry

### Dashboard

- `GET /api/dashboard` - Get dashboard data
- `GET /api/dashboard/render` - Get rendered dashboard

### SLA

- `GET /api/sla` - Get SLA status

### Incidents

- `GET /api/incidents` - Get recent incidents

## Testing

Run the comprehensive test suite:

```bash
python tests.py
```

### Test Coverage (10 Tests)

1. ✅ **Metrics Collection** - Test metric collection
2. ✅ **Metrics Aggregation** - Test aggregation functions
3. ✅ **Alert Rules** - Test rule evaluation
4. ✅ **Alert Firing** - Test alert triggering
5. ✅ **Log Aggregation** - Test log collection
6. ✅ **Log Querying** - Test log search
7. ✅ **SLA Monitoring** - Test SLA tracking
8. ✅ **Incident Detection** - Test incident detection
9. ✅ **Incident Response** - Test automated response
10. ✅ **Aggregators** - Test count, sum, avg

## Educational Notes

### 1. Three Pillars of Observability

**Metrics:**
- Numerical measurements
- Time-series data
- Aggregatable

**Logs:**
- Event records
- Detailed context
- Searchable

**Traces:**
- Request flow
- Distributed tracing
- (Not implemented - advanced)

### 2. Why Alerting?

**Benefits:**
- Early problem detection
- Proactive response
- Reduce downtime
- Improve reliability

### 3. SLA Monitoring

**SLA Components:**
- Target: What you promise (99.9% uptime)
- Actual: What you deliver
- Compliance: Meeting targets

## Production Considerations

For production use:

1. **Metrics:**
   - Use Prometheus
   - Implement exporters
   - Add Grafana dashboards

2. **Alerting:**
   - Use Alertmanager
   - Integrate PagerDuty/Slack
   - Implement escalation

3. **Logging:**
   - Use ELK stack
   - Implement log shipping
   - Add log analysis

4. **Monitoring:**
   - Distributed tracing
   - APM tools
   - Real-time dashboards

## Dependencies

- **Flask 3.0.0** - Web framework
- **psutil 5.9.6** - System metrics
- **python-dotenv 1.0.0** - Environment variables
- **pytest 7.4.3** - Testing framework
- **sqlite3** - Database (built-in)

## License

This project is for educational purposes. Feel free to use and modify as needed.

---

**Happy Monitoring! 🚀**
