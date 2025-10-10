"""
Incident Store
SQLite-based incident storage
"""

import sqlite3
import json
import logging

logger = logging.getLogger(__name__)


class IncidentStore:
    """
    SQLite-based incident storage
    """
    
    def __init__(self, db_path='observability.db'):
        """
        Initialize incident store
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        self._init_database()
        
        logger.info("Incident Store initialized")
    
    def _init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                incident_type TEXT NOT NULL,
                description TEXT,
                severity TEXT,
                detected_at REAL NOT NULL,
                resolved_at REAL,
                response_actions TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_incidents_time ON incidents(detected_at)')
        
        conn.commit()
        conn.close()
    
    def save_incident(self, incident_type, description, severity='medium', response_actions=None):
        """
        Save incident to database
        
        Args:
            incident_type: Type of incident
            description: Incident description
            severity: Incident severity
            response_actions: Actions taken
            
        Returns:
            Incident ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        import time
        detected_at = time.time()
        
        actions_json = json.dumps(response_actions) if response_actions else None
        
        cursor.execute('''
            INSERT INTO incidents (incident_type, description, severity, detected_at, response_actions)
            VALUES (?, ?, ?, ?, ?)
        ''', (incident_type, description, severity, detected_at, actions_json))
        
        incident_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return incident_id
    
    def resolve_incident(self, incident_id):
        """
        Mark incident as resolved
        
        Args:
            incident_id: Incident ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        import time
        resolved_at = time.time()
        
        cursor.execute('''
            UPDATE incidents 
            SET resolved_at = ? 
            WHERE id = ?
        ''', (resolved_at, incident_id))
        
        conn.commit()
        conn.close()
    
    def get_recent_incidents(self, hours=24, limit=100):
        """
        Get recent incidents
        
        Args:
            hours: Hours of history
            limit: Maximum incidents
            
        Returns:
            List of incidents
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        import time
        cutoff_time = time.time() - (hours * 3600)
        
        cursor.execute('''
            SELECT * FROM incidents 
            WHERE detected_at > ? 
            ORDER BY detected_at DESC 
            LIMIT ?
        ''', (cutoff_time, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        incidents = []
        for row in rows:
            incidents.append(dict(row))
        
        return incidents
