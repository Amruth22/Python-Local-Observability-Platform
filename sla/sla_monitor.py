"""
SLA Monitor
Monitors Service Level Agreements
"""

import sqlite3
import logging
import time

logger = logging.getLogger(__name__)


class SLAMonitor:
    """
    SLA monitoring system with SQLite
    """
    
    def __init__(self, db_path='observability.db'):
        """
        Initialize SLA monitor
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        self.sla_definitions = {}
        self._init_database()
        
        logger.info("SLA Monitor initialized")
    
    def _init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sla_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sla_name TEXT NOT NULL,
                is_compliant BOOLEAN NOT NULL,
                actual_value REAL NOT NULL,
                target_value REAL NOT NULL,
                timestamp REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_sla_name_time ON sla_metrics(sla_name, timestamp)')
        
        conn.commit()
        conn.close()
    
    def define_sla(self, name, target, metric_type='uptime'):
        """
        Define an SLA
        
        Args:
            name: SLA name
            target: Target value (e.g., 99.9 for 99.9% uptime)
            metric_type: Type of metric (uptime, error_rate, latency)
        """
        self.sla_definitions[name] = {
            'target': target,
            'metric_type': metric_type
        }
        
        logger.info(f"SLA defined: {name} (target: {target}%)")
    
    def record_sla_metric(self, sla_name, actual_value):
        """
        Record SLA metric
        
        Args:
            sla_name: SLA name
            actual_value: Actual measured value
        """
        if sla_name not in self.sla_definitions:
            logger.warning(f"SLA not defined: {sla_name}")
            return
        
        sla = self.sla_definitions[sla_name]
        target = sla['target']
        
        # Determine compliance
        is_compliant = actual_value >= target
        
        # Save to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = time.time()
        
        cursor.execute('''
            INSERT INTO sla_metrics (sla_name, is_compliant, actual_value, target_value, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (sla_name, is_compliant, actual_value, target, timestamp))
        
        conn.commit()
        conn.close()
        
        logger.debug(f"SLA metric recorded: {sla_name} = {actual_value}% (target: {target}%)")
    
    def get_sla_status(self, sla_name, hours=24):
        """
        Get SLA status
        
        Args:
            sla_name: SLA name
            hours: Hours to analyze
            
        Returns:
            SLA status dictionary
        """
        if sla_name not in self.sla_definitions:
            return None
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_time = time.time() - (hours * 3600)
        
        cursor.execute('''
            SELECT AVG(actual_value) as avg_value, target_value 
            FROM sla_metrics 
            WHERE sla_name = ? AND timestamp > ?
        ''', (sla_name, cutoff_time))
        
        row = cursor.fetchone()
        conn.close()
        
        if row and row[0] is not None:
            avg_value = row[0]
            target = row[1]
            
            return {
                'sla_name': sla_name,
                'current': avg_value,
                'target': target,
                'compliant': avg_value >= target,
                'window_hours': hours
            }
        
        # No data, return target
        sla = self.sla_definitions[sla_name]
        return {
            'sla_name': sla_name,
            'current': 0,
            'target': sla['target'],
            'compliant': False,
            'window_hours': hours
        }
    
    def get_all_sla_status(self, hours=24):
        """
        Get status of all SLAs
        
        Args:
            hours: Hours to analyze
            
        Returns:
            Dictionary of SLA statuses
        """
        statuses = {}
        
        for sla_name in self.sla_definitions.keys():
            statuses[sla_name] = self.get_sla_status(sla_name, hours)
        
        return statuses
    
    def calculate_uptime_percentage(self, total_checks, successful_checks):
        """
        Calculate uptime percentage
        
        Args:
            total_checks: Total health checks
            successful_checks: Successful health checks
            
        Returns:
            Uptime percentage
        """
        if total_checks == 0:
            return 100.0
        
        return (successful_checks / total_checks) * 100
