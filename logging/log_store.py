"""
Log Store
Additional log storage utilities
"""

import sqlite3
import logging as std_logging

logger = std_logging.getLogger(__name__)


class LogStore:
    """
    Log storage utilities
    """
    
    def __init__(self, db_path='observability.db'):
        """
        Initialize log store
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        logger.info("Log Store initialized")
    
    def get_error_count(self, hours=24):
        """
        Get error count
        
        Args:
            hours: Hours of history
            
        Returns:
            Error count
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        import time
        cutoff_time = time.time() - (hours * 3600)
        
        cursor.execute('''
            SELECT COUNT(*) FROM logs 
            WHERE level IN ('ERROR', 'CRITICAL') AND timestamp > ?
        ''', (cutoff_time,))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
    
    def get_log_stats(self, hours=24):
        """
        Get log statistics
        
        Args:
            hours: Hours of history
            
        Returns:
            Log statistics
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        import time
        cutoff_time = time.time() - (hours * 3600)
        
        # Total logs
        cursor.execute('SELECT COUNT(*) FROM logs WHERE timestamp > ?', (cutoff_time,))
        total = cursor.fetchone()[0]
        
        # By level
        cursor.execute('''
            SELECT level, COUNT(*) as count 
            FROM logs 
            WHERE timestamp > ? 
            GROUP BY level
        ''', (cutoff_time,))
        
        by_level = {}
        for row in cursor.fetchall():
            by_level[row[0]] = row[1]
        
        conn.close()
        
        return {
            'total': total,
            'by_level': by_level
        }
