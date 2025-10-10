"""
Alert Store
SQLite-based alert storage
"""

import sqlite3
import json
import logging

logger = logging.getLogger(__name__)


class AlertStore:
    """
    SQLite-based alert storage
    """
    
    def __init__(self, db_path='observability.db'):
        """
        Initialize alert store
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        self._init_database()
        
        logger.info("Alert Store initialized")
    
    def _init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rule_name TEXT NOT NULL,
                metric_name TEXT NOT NULL,
                current_value REAL NOT NULL,
                threshold REAL NOT NULL,
                severity TEXT NOT NULL,
                message TEXT,
                fired_at REAL NOT NULL,
                resolved_at REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_alerts_time 
            ON alerts(fired_at)
        ''')
        
        conn.commit()
        conn.close()
    
    def save_alert(self, alert):
        """
        Save alert to database
        
        Args:
            alert: Alert dictionary
            
        Returns:
            Alert ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO alerts (rule_name, metric_name, current_value, threshold, severity, message, fired_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            alert['rule_name'],
            alert['metric'],
            alert['current_value'],
            alert['threshold'],
            alert['severity'],
            alert['message'],
            alert['fired_at']
        ))
        
        alert_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return alert_id
    
    def get_recent_alerts(self, hours=24, limit=100):
        """
        Get recent alerts
        
        Args:
            hours: Hours of history
            limit: Maximum alerts
            
        Returns:
            List of alerts
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        import time
        cutoff_time = time.time() - (hours * 3600)
        
        cursor.execute('''
            SELECT * FROM alerts 
            WHERE fired_at > ? 
            ORDER BY fired_at DESC 
            LIMIT ?
        ''', (cutoff_time, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        alerts = []
        for row in rows:
            alerts.append(dict(row))
        
        return alerts
