"""
SLA Store
Additional SLA storage utilities
"""

import sqlite3
import logging

logger = logging.getLogger(__name__)


class SLAStore:
    """
    SLA data storage utilities
    """
    
    def __init__(self, db_path='observability.db'):
        """
        Initialize SLA store
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        logger.info("SLA Store initialized")
    
    def get_sla_history(self, sla_name, hours=24):
        """
        Get SLA history
        
        Args:
            sla_name: SLA name
            hours: Hours of history
            
        Returns:
            List of SLA measurements
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        import time
        cutoff_time = time.time() - (hours * 3600)
        
        cursor.execute('''
            SELECT * FROM sla_metrics 
            WHERE sla_name = ? AND timestamp > ? 
            ORDER BY timestamp DESC
        ''', (sla_name, cutoff_time))
        
        rows = cursor.fetchall()
        conn.close()
        
        history = []
        for row in rows:
            history.append({
                'actual_value': row['actual_value'],
                'target_value': row['target_value'],
                'is_compliant': bool(row['is_compliant']),
                'timestamp': row['timestamp']
            })
        
        return history
    
    def get_compliance_rate(self, sla_name, hours=24):
        """
        Get SLA compliance rate
        
        Args:
            sla_name: SLA name
            hours: Hours to analyze
            
        Returns:
            Compliance rate percentage
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        import time
        cutoff_time = time.time() - (hours * 3600)
        
        # Total measurements
        cursor.execute('''
            SELECT COUNT(*) FROM sla_metrics 
            WHERE sla_name = ? AND timestamp > ?
        ''', (sla_name, cutoff_time))
        
        total = cursor.fetchone()[0]
        
        # Compliant measurements
        cursor.execute('''
            SELECT COUNT(*) FROM sla_metrics 
            WHERE sla_name = ? AND timestamp > ? AND is_compliant = 1
        ''', (sla_name, cutoff_time))
        
        compliant = cursor.fetchone()[0]
        
        conn.close()
        
        if total == 0:
            return 100.0
        
        return (compliant / total) * 100
