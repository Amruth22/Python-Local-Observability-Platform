"""
Metrics Collector
Collects system and application metrics
"""

import psutil
import logging
import time

logger = logging.getLogger(__name__)


class MetricsCollector:
    """
    Collects various metrics
    """
    
    def __init__(self):
        """Initialize metrics collector"""
        self.metrics = {}
        self.collection_count = 0
        
        logger.info("Metrics Collector initialized")
    
    def collect_system_metrics(self):
        """
        Collect system metrics (CPU, memory, disk)
        
        Returns:
            Dictionary of system metrics
        """
        metrics = {
            'cpu_usage_percent': psutil.cpu_percent(interval=1),
            'memory_usage_percent': psutil.virtual_memory().percent,
            'memory_used_mb': psutil.virtual_memory().used / 1024 / 1024,
            'disk_usage_percent': psutil.disk_usage('/').percent,
            'timestamp': time.time()
        }
        
        self.collection_count += 1
        
        logger.debug(f"System metrics collected: CPU={metrics['cpu_usage_percent']}%")
        
        return metrics
    
    def collect_metric(self, name, value, labels=None):
        """
        Collect a custom metric
        
        Args:
            name: Metric name
            value: Metric value
            labels: Optional labels dictionary
        """
        if name not in self.metrics:
            self.metrics[name] = []
        
        metric_entry = {
            'value': value,
            'timestamp': time.time(),
            'labels': labels or {}
        }
        
        self.metrics[name].append(metric_entry)
        
        # Keep only recent metrics (last 1000)
        if len(self.metrics[name]) > 1000:
            self.metrics[name] = self.metrics[name][-1000:]
        
        logger.debug(f"Metric collected: {name} = {value}")
    
    def get_metric(self, name, limit=100):
        """
        Get metric values
        
        Args:
            name: Metric name
            limit: Maximum values to return
            
        Returns:
            List of metric values
        """
        if name not in self.metrics:
            return []
        
        return self.metrics[name][-limit:]
    
    def get_latest_value(self, name):
        """
        Get latest value for a metric
        
        Args:
            name: Metric name
            
        Returns:
            Latest value or None
        """
        if name in self.metrics and self.metrics[name]:
            return self.metrics[name][-1]['value']
        
        return None
    
    def get_average(self, name, window_seconds=60):
        """
        Get average value over time window
        
        Args:
            name: Metric name
            window_seconds: Time window in seconds
            
        Returns:
            Average value
        """
        if name not in self.metrics:
            return None
        
        current_time = time.time()
        cutoff_time = current_time - window_seconds
        
        recent_values = [
            m['value'] for m in self.metrics[name]
            if m['timestamp'] >= cutoff_time
        ]
        
        if recent_values:
            return sum(recent_values) / len(recent_values)
        
        return None
    
    def get_all_metrics(self):
        """Get all metric names"""
        return list(self.metrics.keys())
    
    def get_stats(self):
        """Get collector statistics"""
        return {
            'collection_count': self.collection_count,
            'tracked_metrics': len(self.metrics),
            'total_data_points': sum(len(values) for values in self.metrics.values())
        }
