"""
Agent Monitor - Real-time monitoring for AI agents

A comprehensive monitoring solution that provides real-time visibility into AI agent
performance, execution traces, and system metrics with dashboard integration.

Basic Usage:
    import agent_monitor
    
    # Initialize monitoring
    agent_monitor.init(
        api_key="your-api-key-here",
        dashboard_url="https://0f3jus9vnfzq.space.minimax.io"
    )
    
    # Your agent code runs here - monitoring happens automatically
    
Advanced Usage:
    from agent_monitor import AgentMonitor
    
    monitor = AgentMonitor(
        agent_id="my-agent",
        agent_name="My Agent",
        agent_type="autonomous"
    )
    monitor.start_session()
    monitor.log_event("initialization", {"status": "ready"})
    monitor.end_session()
    
Framework Detection:
    - Automatically detects LangChain, LangGraph, and other frameworks
    - Provides zero-configuration monitoring setup
    - Captures execution traces, performance metrics, and errors

Features:
    - Real-time agent registration and status updates
    - Automatic framework detection and instrumentation
    - Performance monitoring and error tracking
    - Dashboard integration with live updates
    - Support for multiple agent frameworks
"""

from .monitor import AgentMonitor, get_global_monitor, set_global_monitor
from .client import AgentClient
from .exceptions import (
    AgentMonitorError,
    ConnectionError,
    AuthenticationError,
    ConfigurationError
)
from .detectors import detect_framework
from .integrations import (
    LangChainIntegration,
    LangGraphIntegration,
    CustomIntegration
)
from .config import init as config_init

__version__ = "1.0.0"
__author__ = "MiniMax"
__email__ = "support@minimax.com"

# Package metadata
__all__ = [
    "AgentMonitor",
    "AgentClient", 
    "AgentMonitorError",
    "ConnectionError",
    "AuthenticationError",
    "ConfigurationError",
    "detect_framework",
    "LangChainIntegration",
    "LangGraphIntegration", 
    "CustomIntegration",
    "init",
    "quick_start"
]

# Global initialization function
def init(
    api_key: str,
    dashboard_url: str,
    timeout: int = 30,
    retry_count: int = 3,
    enable_logging: bool = False
):
    """
    Initialize the agent monitoring system globally.
    
    This function sets up global configuration and enables automatic
    framework detection and monitoring.
    
    Args:
        api_key: API key for dashboard authentication
        dashboard_url: URL of the monitoring dashboard
        timeout: Request timeout in seconds (default: 30)
        retry_count: Number of retry attempts (default: 3)
        enable_logging: Enable debug logging (default: False)
        
    Example:
        import agent_monitor
        
        agent_monitor.init(
            api_key="your-api-key-here",
            dashboard_url="https://0f3jus9vnfzq.space.minimax.io"
        )
        
        # Your agent code runs here - monitoring happens automatically
    """
    # Initialize global configuration
    config_init(
        api_key=api_key,
        dashboard_url=dashboard_url,
        timeout=timeout,
        retry_count=retry_count,
        enable_logging=enable_logging
    )
    
    # Create and start global monitor if it doesn't exist
    global_monitor = get_global_monitor()
    if global_monitor is None:
        global_monitor = AgentMonitor(
            dashboard_url=dashboard_url,
            api_key=api_key,
            agent_name="global_agent",
            auto_detect=True
        )
        set_global_monitor(global_monitor)
        
        # Start monitoring
        try:
            global_monitor.start()
        except Exception as e:
            print(f"Warning: Could not start global monitoring: {e}")

# Quick start helper function
def quick_start(dashboard_url=None, api_key=None, agent_name=None, group_id="default"):
    """
    Quick start function for immediate monitoring setup
    
    Args:
        dashboard_url: URL of the agent dashboard
        api_key: Authentication API key
        agent_name: Name for this agent (auto-generated if not provided)
        group_id: Group identifier for organizing agents
    
    Returns:
        AgentMonitor: Configured and started monitor instance
    
    Example:
        import agent_monitor
        
        # Start monitoring in one line
        monitor = agent_monitor.quick_start(
            dashboard_url="https://your-dashboard.com",
            api_key="your-api-key"
        )
    """
    monitor = AgentMonitor(
        dashboard_url=dashboard_url,
        api_key=api_key,
        agent_name=agent_name,
        group_id=group_id
    )
    monitor.start()
    return monitor
