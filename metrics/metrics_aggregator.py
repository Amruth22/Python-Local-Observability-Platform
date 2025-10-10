"""
Metrics Aggregator
Aggregates metrics for analysis
"""

import logging

logger = logging.getLogger(__name__)


class MetricsAggregator:
    """
    Aggregates metrics for analysis
    """
    
    def __init__(self):
        """Initialize metrics aggregator"""
        logger.info("Metrics Aggregator initialized")
    
    def aggregate_sum(self, metrics):
        """
        Calculate sum of metric values
        
        Args:
            metrics: List of metric entries
            
        Returns:
            Sum of values
        """
        return sum(m['value'] for m in metrics)
    
    def aggregate_avg(self, metrics):
        """
        Calculate average of metric values
        
        Args:
            metrics: List of metric entries
            
        Returns:
            Average value
        """
        if not metrics:
            return 0
        
        return sum(m['value'] for m in metrics) / len(metrics)
    
    def aggregate_min(self, metrics):
        """
        Find minimum metric value
        
        Args:
            metrics: List of metric entries
            
        Returns:
            Minimum value
        """
        if not metrics:
            return None
        
        return min(m['value'] for m in metrics)
    
    def aggregate_max(self, metrics):
        """
        Find maximum metric value
        
        Args:
            metrics: List of metric entries
            
        Returns:
            Maximum value
        """
        if not metrics:
            return None
        
        return max(m['value'] for m in metrics)
    
    def aggregate_percentile(self, metrics, percentile=95):
        """
        Calculate percentile
        
        Args:
            metrics: List of metric entries
            percentile: Percentile to calculate (0-100)
            
        Returns:
            Percentile value
        """
        if not metrics:
            return None
        
        values = sorted([m['value'] for m in metrics])
        index = int(len(values) * (percentile / 100))
        
        return values[min(index, len(values) - 1)]
    
    def aggregate_rate(self, metrics, window_seconds=60):
        """
        Calculate rate (events per second)
        
        Args:
            metrics: List of metric entries
            window_seconds: Time window
            
        Returns:
            Rate per second
        """
        if not metrics:
            return 0
        
        import time
        current_time = time.time()
        cutoff_time = current_time - window_seconds
        
        recent = [m for m in metrics if m['timestamp'] >= cutoff_time]
        
        return len(recent) / window_seconds if window_seconds > 0 else 0
    
    def aggregate_all(self, metrics):
        """
        Calculate all aggregations
        
        Args:
            metrics: List of metric entries
            
        Returns:
            Dictionary of aggregations
        """
        if not metrics:
            return {
                'count': 0,
                'sum': 0,
                'avg': 0,
                'min': None,
                'max': None
            }
        
        return {
            'count': len(metrics),
            'sum': self.aggregate_sum(metrics),
            'avg': self.aggregate_avg(metrics),
            'min': self.aggregate_min(metrics),
            'max': self.aggregate_max(metrics),
            'p95': self.aggregate_percentile(metrics, 95)
        }
