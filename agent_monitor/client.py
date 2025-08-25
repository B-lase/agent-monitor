"""
Agent Client - Core HTTP client for communicating with the dashboard API

Handles all communication with the Supabase backend including agent registration,
status updates, log submission, and heartbeat management.
"""

import json
import time
import uuid
import threading
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List

import requests
from .exceptions import ConnectionError, AuthenticationError, AgentMonitorError


class AgentClient:
    """
    Core client for communicating with the agent monitoring dashboard API.
    
    This class handles all HTTP communication with the Supabase backend,
    including agent registration, status updates, and log submission.
    """
    
    def __init__(self, dashboard_url: str, api_key: str, timeout: int = 30):
        """
        Initialize the agent client.
        
        Args:
            dashboard_url: Base URL of the dashboard
            api_key: Supabase API key for authentication
            timeout: Request timeout in seconds
        """
        self.dashboard_url = dashboard_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        
        # Extract Supabase URL from dashboard URL
        if 'minimax.io' in dashboard_url:
            # For deployed dashboards, use the known Supabase URL  
            self.supabase_url = "https://ybhjabiromsmnqrzmnab.supabase.co"
            # Use the provided API key for authentication
            # This should be a service role key for agent monitoring
            self.headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}',
                'apikey': api_key
            }
        else:
            # For custom deployments, try to extract from URL
            self.supabase_url = dashboard_url.replace('/dashboard', '')
            self.headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}',
                'apikey': api_key
            }
        
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # Agent info
        self.agent_id = None
        self.user_id = None
        
    def register_agent(self, agent_name: str, group_id: str, metadata: Optional[Dict] = None) -> str:
        """
        Register a new agent with the dashboard.
        
        Args:
            agent_name: Human-readable name for the agent
            group_id: Group identifier for organizing agents
            metadata: Additional metadata to store with the agent
            
        Returns:
            str: The registered agent ID
            
        Raises:
            ConnectionError: If unable to connect to the API
            AuthenticationError: If API key is invalid
            AgentMonitorError: If registration fails
        """
        if not self.agent_id:
            # Generate unique agent ID
            self.agent_id = f"{agent_name.lower().replace(' ', '_')}_{int(time.time())}_{str(uuid.uuid4())[:8]}"
        
        agent_data = {
            'agent_id': self.agent_id,
            'name': agent_name,
            'group_id': group_id,
            'status': 'running',
            'connection_status': 'connected',
            'is_active': True,
            'last_seen': datetime.now(timezone.utc).isoformat(),
            'last_heartbeat': datetime.now(timezone.utc).isoformat(),
            'metadata': metadata or {},
            'position_x': 100,  # Default position
            'position_y': 100
        }
        
        try:
            response = self.session.post(
                f"{self.supabase_url}/rest/v1/agents",
                json=agent_data,
                timeout=self.timeout
            )
            
            if response.status_code == 401:
                raise AuthenticationError("Invalid API key or insufficient permissions")
            elif response.status_code == 409:
                # Agent already exists, update it instead
                return self._update_agent_status('running')
            elif not response.ok:
                raise AgentMonitorError(f"Agent registration failed: {response.status_code} {response.text}")
                
            return self.agent_id
            
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to connect to dashboard API: {str(e)}")
    
    def send_log(self, message_type: str, message: str, metadata: Optional[Dict] = None):
        """
        Send a log message to the dashboard.
        
        Args:
            message_type: Type of message (e.g., 'info', 'error', 'debug', 'trace')
            message: The log message content
            metadata: Additional structured data
            
        Raises:
            AgentMonitorError: If log submission fails
        """
        if not self.agent_id:
            raise AgentMonitorError("Agent must be registered before sending logs")
        
        log_data = {
            'agent_id': self.agent_id,
            'message_type': message_type,
            'message': message,
            'metadata': metadata or {},
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        try:
            response = self.session.post(
                f"{self.supabase_url}/rest/v1/agent_logs",
                json=log_data,
                timeout=self.timeout
            )
            
            if not response.ok:
                # Log failures shouldn't break the agent, just warn
                print(f"Warning: Failed to send log to dashboard: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"Warning: Failed to connect to dashboard for logging: {str(e)}")
    
    def update_status(self, status: str, metadata: Optional[Dict] = None):
        """
        Update the agent's status.
        
        Args:
            status: New status ('running', 'idle', 'error', 'offline')
            metadata: Additional metadata to update
        """
        self._update_agent_status(status, metadata)
    
    def _update_agent_status(self, status: str, metadata: Optional[Dict] = None) -> str:
        """
        Internal method to update agent status.
        """
        if not self.agent_id:
            raise AgentMonitorError("Agent must be registered before updating status")
        
        update_data = {
            'status': status,
            'last_seen': datetime.now(timezone.utc).isoformat(),
            'last_heartbeat': datetime.now(timezone.utc).isoformat(),
            'updated_at': datetime.now(timezone.utc).isoformat()
        }
        
        if metadata:
            update_data['metadata'] = metadata
        
        try:
            response = self.session.patch(
                f"{self.supabase_url}/rest/v1/agents?agent_id=eq.{self.agent_id}",
                json=update_data,
                timeout=self.timeout
            )
            
            if not response.ok:
                print(f"Warning: Failed to update agent status: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"Warning: Failed to connect to dashboard for status update: {str(e)}")
        
        return self.agent_id
    
    def send_heartbeat(self):
        """
        Send a heartbeat to indicate the agent is still alive.
        """
        self._update_agent_status('running')
    
    def shutdown(self):
        """
        Gracefully shutdown the agent connection.
        """
        if self.agent_id:
            self._update_agent_status('offline')
        if self.session:
            self.session.close()


class HeartbeatThread(threading.Thread):
    """
    Background thread for sending periodic heartbeats.
    """
    
    def __init__(self, client: AgentClient, interval: int = 30):
        super().__init__(daemon=True)
        self.client = client
        self.interval = interval
        self.running = False
    
    def run(self):
        self.running = True
        while self.running:
            try:
                self.client.send_heartbeat()
                time.sleep(self.interval)
            except Exception as e:
                print(f"Heartbeat error: {e}")
                time.sleep(self.interval)
    
    def stop(self):
        self.running = False
