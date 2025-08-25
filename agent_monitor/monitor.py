"""
AgentMonitor - Main monitoring class with framework integration

Provides the high-level monitoring interface that users interact with.
Handles framework detection, automatic instrumentation, and lifecycle management.
"""

import os
import sys
import atexit
import socket
from typing import Optional, Dict, Any, Callable
from uuid import uuid4

from .client import AgentClient, HeartbeatThread
from .detectors import detect_framework, get_environment_info
from .exceptions import ConfigurationError, AgentMonitorError
from .integrations import get_integration_for_framework


class AgentMonitor:
    """
    Main monitoring class that provides comprehensive agent monitoring capabilities.
    
    This class automatically detects AI frameworks and provides monitoring
    with minimal configuration required from the user.
    
    Example:
        monitor = AgentMonitor(
            dashboard_url="https://your-dashboard.com",
            api_key="your-api-key"
        )
        monitor.start()
        
        # Your agent code runs here
        # Monitoring happens automatically
    """
    
    def __init__(
        self,
        dashboard_url: Optional[str] = None,
        api_key: Optional[str] = None,
        agent_name: Optional[str] = None,
        group_id: str = "default",
        heartbeat_interval: int = 30,
        auto_detect: bool = True,
        metadata: Optional[Dict] = None
    ):
        """
        Initialize the agent monitor.
        
        Args:
            dashboard_url: URL of the monitoring dashboard
            api_key: API key for authentication
            agent_name: Name for this agent (auto-generated if not provided)
            group_id: Group identifier for organizing agents
            heartbeat_interval: Seconds between heartbeat signals
            auto_detect: Whether to automatically detect frameworks
            metadata: Additional metadata to include with the agent
        """
        # Configuration
        self.dashboard_url = dashboard_url or os.getenv('AGENT_MONITOR_URL')
        self.api_key = api_key or os.getenv('AGENT_MONITOR_API_KEY')
        self.agent_name = agent_name or self._generate_agent_name()
        self.group_id = group_id
        self.heartbeat_interval = heartbeat_interval
        self.auto_detect = auto_detect
        self.metadata = metadata or {}
        
        # Validation
        if not self.dashboard_url:
            raise ConfigurationError(
                "Dashboard URL is required. Set via parameter or AGENT_MONITOR_URL environment variable."
            )
        
        if not self.api_key:
            raise ConfigurationError(
                "API key is required. Set via parameter or AGENT_MONITOR_API_KEY environment variable."
            )
        
        # Internal state
        self.client = None
        self.heartbeat_thread = None
        self.framework_info = None
        self.integration = None
        self.is_started = False
        
        # Event handlers
        self.on_start = None
        self.on_stop = None
        self.on_error = None
        
        # Register shutdown handler
        atexit.register(self._cleanup)
    
    def start(self) -> str:
        """
        Start the monitoring system.
        
        Returns:
            str: The agent ID assigned by the dashboard
            
        Raises:
            AgentMonitorError: If starting fails
        """
        if self.is_started:
            self.log("warning", "Monitor already started")
            return self.client.agent_id if self.client else None
        
        try:
            # Detect framework if enabled
            if self.auto_detect:
                self.framework_info = detect_framework()
                self.log("info", f"Detected framework: {self.framework_info.get('name', 'unknown')}")
            
            # Initialize client
            self.client = AgentClient(
                dashboard_url=self.dashboard_url,
                api_key=self.api_key
            )
            
            # Prepare metadata
            agent_metadata = {
                **self.metadata,
                'framework': self.framework_info,
                'environment': get_environment_info(),
                'host': socket.gethostname(),
                'pid': os.getpid()
            }
            
            # Register agent
            agent_id = self.client.register_agent(
                agent_name=self.agent_name,
                group_id=self.group_id,
                metadata=agent_metadata
            )
            
            # Start heartbeat
            if self.heartbeat_interval > 0:
                self.heartbeat_thread = HeartbeatThread(
                    client=self.client,
                    interval=self.heartbeat_interval
                )
                self.heartbeat_thread.start()
            
            # Setup framework integration
            if self.framework_info and self.framework_info.get('available'):
                self.integration = get_integration_for_framework(
                    self.framework_info['name'],
                    self
                )
                if self.integration:
                    self.integration.setup()
            
            self.is_started = True
            self.log("info", f"Agent monitoring started with ID: {agent_id}")
            
            # Call start handler if set
            if self.on_start:
                self.on_start(agent_id)
            
            return agent_id
            
        except Exception as e:
            error_msg = f"Failed to start monitoring: {str(e)}"
            if self.on_error:
                self.on_error(error_msg)
            raise AgentMonitorError(error_msg)
    
    def stop(self):
        """
        Stop the monitoring system.
        """
        if not self.is_started:
            return
        
        try:
            self.log("info", "Stopping agent monitoring")
            
            # Stop integration
            if self.integration:
                self.integration.cleanup()
            
            # Stop heartbeat
            if self.heartbeat_thread:
                self.heartbeat_thread.stop()
                self.heartbeat_thread = None
            
            # Shutdown client
            if self.client:
                self.client.shutdown()
                self.client = None
            
            self.is_started = False
            
            # Call stop handler if set
            if self.on_stop:
                self.on_stop()
                
        except Exception as e:
            print(f"Error during monitoring shutdown: {e}")
    
    def log(self, level: str, message: str, metadata: Optional[Dict] = None):
        """
        Send a log message to the dashboard.
        
        Args:
            level: Log level ('debug', 'info', 'warning', 'error', 'trace')
            message: Log message content
            metadata: Additional structured data
        """
        if not self.client:
            print(f"[{level.upper()}] {message}")  # Fallback to console
            return
        
        try:
            self.client.send_log(
                message_type=level,
                message=message,
                metadata=metadata
            )
        except Exception as e:
            print(f"Failed to send log: {e}")
    
    def trace(self, operation: str, metadata: Optional[Dict] = None):
        """
        Log an execution trace.
        
        Args:
            operation: Description of the operation being traced
            metadata: Additional trace data
        """
        self.log("trace", operation, metadata)
    
    def error(self, error: Exception, metadata: Optional[Dict] = None):
        """
        Log an error.
        
        Args:
            error: The exception that occurred
            metadata: Additional error context
        """
        error_metadata = {
            'error_type': type(error).__name__,
            'error_message': str(error),
            **(metadata or {})
        }
        
        self.log("error", f"Error: {str(error)}", error_metadata)
    
    def update_status(self, status: str, metadata: Optional[Dict] = None):
        """
        Update the agent's status.
        
        Args:
            status: New status ('running', 'idle', 'error', 'offline')
            metadata: Additional status metadata
        """
        if self.client:
            self.client.update_status(status, metadata)
    
    def _generate_agent_name(self) -> str:
        """
        Generate a default agent name based on the environment.
        """
        hostname = socket.gethostname()
        pid = os.getpid()
        random_suffix = str(uuid4())[:8]
        
        return f"agent_{hostname}_{pid}_{random_suffix}"
    
    def _cleanup(self):
        """
        Cleanup method called on exit.
        """
        if self.is_started:
            self.stop()


# Global monitor instance for convenience
_global_monitor = None


def get_global_monitor() -> Optional[AgentMonitor]:
    """
    Get the global monitor instance if it exists.
    
    Returns:
        AgentMonitor or None if not initialized
    """
    return _global_monitor


def set_global_monitor(monitor: AgentMonitor):
    """
    Set the global monitor instance.
    
    Args:
        monitor: AgentMonitor instance to set as global
    """
    global _global_monitor
    _global_monitor = monitor
