"""
Metrics Store
SQLite-based metrics storage
"""

import sqlite3
import json
import logging

logger = logging.getLogger(__name__)


class MetricsStore:
    """
    SQLite-based metrics storage
    """
    
    def __init__(self, db_path='observability.db'):
        """
        Initialize metrics store
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        self._init_database()
        
        logger.info("Metrics Store initialized")
    
    def _init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT NOT NULL,
                metric_value REAL NOT NULL,
                labels TEXT,
                timestamp REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_metrics_name_time 
            ON metrics(metric_name, timestamp)
        ''')
        
        conn.commit()
        conn.close()
    
    def save_metric(self, name, value, labels=None, timestamp=None):
        """
        Save metric to database
        
        Args:
            name: Metric name
            value: Metric value
            labels: Optional labels
            timestamp: Optional timestamp
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if timestamp is None:
            timestamp = time.time()
        
        labels_json = json.dumps(labels) if labels else None
        
        cursor.execute('''
            INSERT INTO metrics (metric_name, metric_value, labels, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (name, value, labels_json, timestamp))
        
        conn.commit()
        conn.close()
    
    def get_metrics(self, name, hours=24, limit=1000):
        """
        Get metrics from database
        
        Args:
            name: Metric name
            hours: Hours of history
            limit: Maximum records
            
        Returns:
            List of metrics
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        import time
        cutoff_time = time.time() - (hours * 3600)
        
        cursor.execute('''
            SELECT * FROM metrics 
            WHERE metric_name = ? AND timestamp > ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (name, cutoff_time, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        metrics = []
        for row in rows:
            metrics.append({
                'value': row['metric_value'],
                'timestamp': row['timestamp'],
                'labels': json.loads(row['labels']) if row['labels'] else {}
            })
        
        return metrics
    
    def delete_old_metrics(self, hours=24):
        """
        Delete metrics older than specified hours
        
        Args:
            hours: Hours to retain
            
        Returns:
            Number of deleted metrics
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        import time
        cutoff_time = time.time() - (hours * 3600)
        
        cursor.execute('DELETE FROM metrics WHERE timestamp < ?', (cutoff_time,))
        deleted = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        logger.info(f"Deleted {deleted} old metrics")
        
        return deleted


import time
