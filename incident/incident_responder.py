"""
Incident Responder
Automated incident response
"""

import logging

logger = logging.getLogger(__name__)


class IncidentResponder:
    """
    Automated incident response system
    """
    
    def __init__(self):
        """Initialize incident responder"""
        self.playbooks = {}
        self.response_history = []
        
        logger.info("Incident Responder initialized")
    
    def add_playbook(self, incident_type, actions):
        """
        Add response playbook
        
        Args:
            incident_type: Type of incident
            actions: List of action names
        """
        self.playbooks[incident_type] = actions
        logger.info(f"Playbook added for {incident_type}: {actions}")
    
    def respond(self, incident_type, context=None):
        """
        Respond to incident
        
        Args:
            incident_type: Type of incident
            context: Optional context data
            
        Returns:
            List of executed actions
        """
        if incident_type not in self.playbooks:
            logger.warning(f"No playbook for incident: {incident_type}")
            return []
        
        actions = self.playbooks[incident_type]
        executed_actions = []
        
        logger.warning(f"Responding to incident: {incident_type}")
        
        for action in actions:
            try:
                result = self._execute_action(action, context)
                executed_actions.append({
                    'action': action,
                    'result': result,
                    'success': True
                })
                logger.info(f"Action executed: {action}")
            except Exception as e:
                executed_actions.append({
                    'action': action,
                    'error': str(e),
                    'success': False
                })
                logger.error(f"Action failed: {action} - {e}")
        
        # Record response
        self.response_history.append({
            'incident_type': incident_type,
            'actions': executed_actions,
            'context': context,
            'timestamp': time.time()
        })
        
        return executed_actions
    
    def _execute_action(self, action, context):
        """
        Execute a response action
        
        Args:
            action: Action name
            context: Context data
            
        Returns:
            Action result
        """
        if action == 'log_incident':
            logger.warning(f"INCIDENT: {context}")
            return 'Incident logged'
        
        elif action == 'send_alert':
            print(f"\n🚨 ALERT: Incident detected - {context}")
            return 'Alert sent'
        
        elif action == 'restart_service':
            logger.info("Simulating service restart...")
            return 'Service restart initiated'
        
        elif action == 'scale_up':
            logger.info("Simulating scale up...")
            return 'Scale up initiated'
        
        elif action == 'notify_team':
            logger.info("Simulating team notification...")
            return 'Team notified'
        
        else:
            logger.warning(f"Unknown action: {action}")
            return f'Unknown action: {action}'
    
    def get_response_history(self, limit=100):
        """Get response history"""
        return self.response_history[-limit:]


import time
