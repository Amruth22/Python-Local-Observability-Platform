"""
Comprehensive Unit Tests for Local Observability Platform
Tests metrics, alerts, logs, SLA, incidents, and dashboard
"""

import unittest
import os
import time
from metrics.metrics_collector import MetricsCollector
from metrics.metrics_aggregator import MetricsAggregator
from alerting.alert_manager import AlertManager
from alerting.alert_store import AlertStore
from logging.log_aggregator import LogAggregator
from sla.sla_monitor import SLAMonitor
from incident.incident_detector import IncidentDetector
from incident.incident_responder import IncidentResponder
from incident.incident_store import IncidentStore
from aggregation.aggregators import CountAggregator, SumAggregator, AvgAggregator


class ObservabilityPlatformTestCase(unittest.TestCase):
    """Unit tests for Local Observability Platform"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test configuration"""
        print("\n" + "=" * 60)
        print("Local Observability Platform - Unit Test Suite")
        print("=" * 60)
        print("Testing: Metrics, Alerts, Logs, SLA, Incidents")
        print("=" * 60 + "\n")
        
        # Use test database
        cls.db_path = 'test_observability.db'
        if os.path.exists(cls.db_path):
            os.remove(cls.db_path)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after tests"""
        if os.path.exists(cls.db_path):
            os.remove(cls.db_path)
    
    # Test 1: Metrics Collection
    def test_01_metrics_collection(self):
        """Test metrics collection"""
        print("\n1. Testing metrics collection...")
        
        collector = MetricsCollector()
        
        # Collect system metrics
        system_metrics = collector.collect_system_metrics()
        
        self.assertIn('cpu_usage_percent', system_metrics)
        self.assertIn('memory_usage_percent', system_metrics)
        print(f"   [EMOJI] System metrics collected")
        
        # Collect custom metric
        collector.collect_metric('test_metric', 42)
        
        value = collector.get_latest_value('test_metric')
        self.assertEqual(value, 42)
        print(f"   [EMOJI] Custom metric: test_metric = {value}")
    
    # Test 2: Metrics Aggregation
    def test_02_metrics_aggregation(self):
        """Test metrics aggregation"""
        print("\n2. Testing metrics aggregation...")
        
        aggregator = MetricsAggregator()
        
        metrics = [
            {'value': 10, 'timestamp': time.time()},
            {'value': 20, 'timestamp': time.time()},
            {'value': 30, 'timestamp': time.time()}
        ]
        
        # Test aggregations
        total = aggregator.aggregate_sum(metrics)
        self.assertEqual(total, 60)
        print(f"   [EMOJI] Sum: {total}")
        
        avg = aggregator.aggregate_avg(metrics)
        self.assertEqual(avg, 20)
        print(f"   [EMOJI] Avg: {avg}")
        
        min_val = aggregator.aggregate_min(metrics)
        self.assertEqual(min_val, 10)
        print(f"   [EMOJI] Min: {min_val}")
    
    # Test 3: Alert Rules
    def test_03_alert_rules(self):
        """Test alert rule evaluation"""
        print("\n3. Testing alert rules...")
        
        alert_manager = AlertManager()
        
        # Add rule
        alert_manager.add_rule(
            name='test_alert',
            metric='cpu_usage',
            condition='greater_than',
            threshold=80,
            severity='warning'
        )
        
        print("   [EMOJI] Alert rule added")
        
        # Test evaluation
        should_fire = alert_manager.evaluate_rule('test_alert', 85)
        self.assertTrue(should_fire)
        print(f"   [EMOJI] Rule evaluation: {should_fire} (85 > 80)")
        
        should_not_fire = alert_manager.evaluate_rule('test_alert', 75)
        self.assertFalse(should_not_fire)
        print(f"   [EMOJI] Rule evaluation: {should_not_fire} (75 < 80)")
    
    # Test 4: Alert Firing
    def test_04_alert_firing(self):
        """Test alert firing"""
        print("\n4. Testing alert firing...")
        
        alert_manager = AlertManager()
        collector = MetricsCollector()
        
        # Add rule
        alert_manager.add_rule('test', 'metric1', 'greater_than', 50, 'warning')
        
        # Collect metric that triggers alert
        collector.collect_metric('metric1', 75)
        
        # Evaluate
        fired = alert_manager.evaluate_all_rules(collector)
        
        self.assertIn('test', fired)
        print(f"   [EMOJI] Alert fired: {fired}")
        
        # Check active alerts
        active = alert_manager.get_active_alerts()
        self.assertEqual(len(active), 1)
        print(f"   [EMOJI] Active alerts: {len(active)}")
    
    # Test 5: Log Aggregation
    def test_05_log_aggregation(self):
        """Test log aggregation"""
        print("\n5. Testing log aggregation...")
        
        log_agg = LogAggregator(self.db_path)
        
        # Log messages
        log_agg.log('INFO', 'Test info message')
        log_agg.log('ERROR', 'Test error message')
        log_agg.log('WARNING', 'Test warning message')
        
        print("   [EMOJI] 3 log entries recorded")
        
        # Get logs
        all_logs = log_agg.get_logs(hours=24)
        self.assertGreaterEqual(len(all_logs), 3)
        print(f"   [EMOJI] Retrieved {len(all_logs)} logs")
        
        # Get error logs
        errors = log_agg.get_logs(level='ERROR', hours=24)
        self.assertGreaterEqual(len(errors), 1)
        print(f"   [EMOJI] Error logs: {len(errors)}")
    
    # Test 6: Log Querying
    def test_06_log_querying(self):
        """Test log querying"""
        print("\n6. Testing log querying...")
        
        log_agg = LogAggregator(self.db_path)
        
        # Get log counts
        counts = log_agg.get_log_count_by_level(hours=24)
        
        self.assertIsInstance(counts, dict)
        print(f"   [EMOJI] Log counts: {counts}")
    
    # Test 7: SLA Monitoring
    def test_07_sla_monitoring(self):
        """Test SLA monitoring"""
        print("\n7. Testing SLA monitoring...")
        
        sla_monitor = SLAMonitor(self.db_path)
        
        # Define SLA
        sla_monitor.define_sla('test_sla', target=99.0)
        
        # Record metrics
        sla_monitor.record_sla_metric('test_sla', 99.5)
        sla_monitor.record_sla_metric('test_sla', 99.8)
        
        print("   [EMOJI] SLA metrics recorded")
        
        # Get status
        status = sla_monitor.get_sla_status('test_sla')
        
        self.assertIsNotNone(status)
        self.assertTrue(status['compliant'])
        print(f"   [EMOJI] SLA compliant: {status['compliant']}")
    
    # Test 8: Incident Detection
    def test_08_incident_detection(self):
        """Test incident detection"""
        print("\n8. Testing incident detection...")
        
        detector = IncidentDetector()
        
        # Add detection rule
        detector.add_detection_rule(
            'test_incident',
            lambda m, a, l: len(a) > 0,  # Incident if any alerts
            'Test incident'
        )
        
        print("   [EMOJI] Detection rule added")
        
        # Detect with alerts
        incidents = detector.detect_incidents({}, [{'alert': 'test'}], [])
        
        self.assertEqual(len(incidents), 1)
        print(f"   [EMOJI] Incidents detected: {len(incidents)}")
    
    # Test 9: Incident Response
    def test_09_incident_response(self):
        """Test automated incident response"""
        print("\n9. Testing incident response...")
        
        responder = IncidentResponder()
        
        # Add playbook
        responder.add_playbook('test_incident', ['log_incident', 'send_alert'])
        
        # Respond
        actions = responder.respond('test_incident', context={'test': 'data'})
        
        self.assertEqual(len(actions), 2)
        print(f"   [EMOJI] Actions executed: {len(actions)}")
        
        # Check history
        history = responder.get_response_history()
        self.assertGreaterEqual(len(history), 1)
        print(f"   [EMOJI] Response history: {len(history)} entries")
    
    # Test 10: Aggregators
    def test_10_aggregators(self):
        """Test aggregator functions"""
        print("\n10. Testing aggregators...")
        
        # Count aggregator
        count_agg = CountAggregator()
        count_agg.update({'value': 1})
        count_agg.update({'value': 2})
        
        self.assertEqual(count_agg.get_result(), 2)
        print(f"   [EMOJI] Count: {count_agg.get_result()}")
        
        # Sum aggregator
        sum_agg = SumAggregator('value')
        sum_agg.update({'value': 10})
        sum_agg.update({'value': 20})
        
        self.assertEqual(sum_agg.get_result(), 30)
        print(f"   [EMOJI] Sum: {sum_agg.get_result()}")
        
        # Avg aggregator
        avg_agg = AvgAggregator('value')
        avg_agg.update({'value': 10})
        avg_agg.update({'value': 20})
        
        self.assertEqual(avg_agg.get_result(), 15)
        print(f"   [EMOJI] Avg: {avg_agg.get_result()}")


def run_tests():
    """Run all unit tests"""
    # Create test suite
    test_suite = unittest.TestLoader().loadTestsFromTestCase(ObservabilityPlatformTestCase)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.testsRun > 0:
        success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100)
        print(f"Success rate: {success_rate:.1f}%")
    
    if result.failures:
        print("\n[EMOJI] FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print("\n[EMOJI] ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    if not result.failures and not result.errors:
        print("\n[EMOJI] ALL TESTS PASSED! [EMOJI]")
    
    print("=" * 60)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("Local Observability Platform - Unit Test Suite")
    print("=" * 60)
    
    try:
        success = run_tests()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n[EMOJI]️  Tests interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n\n[EMOJI] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
