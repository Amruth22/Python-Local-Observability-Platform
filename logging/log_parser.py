"""
Log Parser
Parses and analyzes log entries
"""

import re
import logging as std_logging

logger = std_logging.getLogger(__name__)


class LogParser:
    """
    Log parsing and analysis
    """
    
    def __init__(self):
        """Initialize log parser"""
        logger.info("Log Parser initialized")
    
    def parse_log_line(self, log_line):
        """
        Parse a log line
        
        Args:
            log_line: Log line string
            
        Returns:
            Parsed log dictionary
        """
        # Simple log format: [LEVEL] timestamp - message
        pattern = r'\[(\w+)\]\s+([\d\-:\s]+)\s+-\s+(.+)'
        
        match = re.match(pattern, log_line)
        
        if match:
            return {
                'level': match.group(1),
                'timestamp': match.group(2),
                'message': match.group(3)
            }
        
        return {
            'level': 'UNKNOWN',
            'timestamp': None,
            'message': log_line
        }
    
    def extract_errors(self, logs):
        """
        Extract error logs
        
        Args:
            logs: List of log entries
            
        Returns:
            List of error logs
        """
        return [log for log in logs if log.get('level') in ['ERROR', 'CRITICAL']]
    
    def search_logs(self, logs, keyword):
        """
        Search logs for keyword
        
        Args:
            logs: List of log entries
            keyword: Keyword to search
            
        Returns:
            Matching logs
        """
        return [log for log in logs if keyword.lower() in log.get('message', '').lower()]
