"""
Log Aggregator
Aggregates and stores application logs
"""

import sqlite3
import logging as std_logging
import time

logger = std_logging.getLogger(__name__)


class LogAggregator:
    """
    Log aggregation system with SQLite
    """
    
    def __init__(self, db_path='observability.db'):
        """
        Initialize log aggregator
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        self._init_database()
        
        logger.info("Log Aggregator initialized")
    
    def _init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                level TEXT NOT NULL,
                message TEXT NOT NULL,
                source TEXT,
                timestamp REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_logs_level_time ON logs(level, timestamp)')
        
        conn.commit()
        conn.close()
    
    def log(self, level, message, source=None):
        """
        Log a message
        
        Args:
            level: Log level (INFO, WARNING, ERROR, CRITICAL)
            message: Log message
            source: Optional source identifier
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = time.time()
        
        cursor.execute('''
            INSERT INTO logs (level, message, source, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (level, message, source, timestamp))
        
        conn.commit()
        conn.close()
        
        logger.debug(f"Log recorded: [{level}] {message}")
    
    def get_logs(self, level=None, hours=24, limit=1000):
        """
        Get logs from database
        
        Args:
            level: Optional level filter
            hours: Hours of history
            limit: Maximum logs
            
        Returns:
            List of logs
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cutoff_time = time.time() - (hours * 3600)
        
        if level:
            cursor.execute('''
                SELECT * FROM logs 
                WHERE level = ? AND timestamp > ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (level, cutoff_time, limit))
        else:
            cursor.execute('''
                SELECT * FROM logs 
                WHERE timestamp > ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (cutoff_time, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        logs = []
        for row in rows:
            logs.append({
                'id': row['id'],
                'level': row['level'],
                'message': row['message'],
                'source': row['source'],
                'timestamp': row['timestamp']
            })
        
        return logs
    
    def get_log_count_by_level(self, hours=24):
        """
        Get log count by level
        
        Args:
            hours: Hours of history
            
        Returns:
            Dictionary of counts by level
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_time = time.time() - (hours * 3600)
        
        cursor.execute('''
            SELECT level, COUNT(*) as count 
            FROM logs 
            WHERE timestamp > ? 
            GROUP BY level
        ''', (cutoff_time,))
        
        rows = cursor.fetchall()
        conn.close()
        
        counts = {}
        for row in rows:
            counts[row[0]] = row[1]
        
        return counts
    
    def delete_old_logs(self, days=7):
        """
        Delete old logs
        
        Args:
            days: Days to retain
            
        Returns:
            Number of deleted logs
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_time = time.time() - (days * 24 * 3600)
        
        cursor.execute('DELETE FROM logs WHERE timestamp < ?', (cutoff_time,))
        deleted = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        logger.info(f"Deleted {deleted} old logs")
        
        return deleted
