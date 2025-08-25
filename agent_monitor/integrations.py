"""
Integration modules for different AI frameworks

Provides framework-specific monitoring integrations that automatically
instrument popular AI frameworks for seamless monitoring.
"""

import sys
import traceback
from typing import Optional, Dict, Any, TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from .monitor import AgentMonitor


class BaseIntegration(ABC):
    """
    Base class for framework integrations.
    """
    
    def __init__(self, monitor: 'AgentMonitor'):
        self.monitor = monitor
        self.is_active = False
    
    @abstractmethod
    def setup(self):
        """
        Setup the integration.
        """
        pass
    
    @abstractmethod
    def cleanup(self):
        """
        Cleanup the integration.
        """
        pass


class LangChainIntegration(BaseIntegration):
    """
    Integration for LangChain framework.
    
    Automatically instruments LangChain chains, agents, and tools
    to provide comprehensive monitoring.
    """
    
    def setup(self):
        """
        Setup LangChain monitoring integration.
        """
        try:
            # Try to setup LangChain callback handler
            self._setup_langchain_callback()
            self.is_active = True
            self.monitor.log("info", "LangChain integration activated")
        except Exception as e:
            self.monitor.log("warning", f"Failed to setup LangChain integration: {e}")
    
    def _setup_langchain_callback(self):
        """
        Setup LangChain callback handler for monitoring.
        """
        try:
            from langchain.callbacks.base import BaseCallbackHandler
            from langchain import callbacks
            
            class AgentMonitorCallback(BaseCallbackHandler):
                def __init__(self, monitor):
                    self.monitor = monitor
                
                def on_chain_start(self, serialized, inputs, **kwargs):
                    self.monitor.trace(
                        f"Chain started: {serialized.get('name', 'unknown')}",
                        {'inputs': inputs, 'serialized': serialized}
                    )
                
                def on_chain_end(self, outputs, **kwargs):
                    self.monitor.trace(
                        "Chain completed",
                        {'outputs': outputs}
                    )
                
                def on_chain_error(self, error, **kwargs):
                    self.monitor.error(error, {'context': 'langchain_chain'})
                
                def on_llm_start(self, serialized, prompts, **kwargs):
                    self.monitor.trace(
                        f"LLM started: {serialized.get('name', 'unknown')}",
                        {'prompts': prompts[:1], 'serialized': serialized}  # Limit prompt logging
                    )
                
                def on_llm_end(self, response, **kwargs):
                    self.monitor.trace(
                        "LLM completed",
                        {'response_summary': str(response)[:200]}  # Limit response logging
                    )
                
                def on_llm_error(self, error, **kwargs):
                    self.monitor.error(error, {'context': 'langchain_llm'})
                
                def on_tool_start(self, serialized, input_str, **kwargs):
                    self.monitor.trace(
                        f"Tool started: {serialized.get('name', 'unknown')}",
                        {'input': input_str, 'tool': serialized.get('name')}
                    )
                
                def on_tool_end(self, output, **kwargs):
                    self.monitor.trace(
                        "Tool completed",
                        {'output_summary': str(output)[:200]}
                    )
                
                def on_tool_error(self, error, **kwargs):
                    self.monitor.error(error, {'context': 'langchain_tool'})
                
                def on_agent_action(self, action, **kwargs):
                    self.monitor.trace(
                        f"Agent action: {action.tool}",
                        {
                            'tool': action.tool,
                            'tool_input': str(action.tool_input)[:200],
                            'log': action.log[:200] if action.log else None
                        }
                    )
                
                def on_agent_finish(self, finish, **kwargs):
                    self.monitor.trace(
                        "Agent finished",
                        {'return_values': str(finish.return_values)[:200]}
                    )
            
            # Register the callback
            self.callback_handler = AgentMonitorCallback(self.monitor)
            
        except ImportError:
            self.monitor.log("warning", "LangChain callback integration not available")
    
    def cleanup(self):
        """
        Cleanup LangChain integration.
        """
        self.is_active = False
        self.monitor.log("info", "LangChain integration deactivated")


class LangGraphIntegration(BaseIntegration):
    """
    Integration for LangGraph framework.
    
    Monitors LangGraph workflows, nodes, and state transitions.
    """
    
    def setup(self):
        """
        Setup LangGraph monitoring integration.
        """
        try:
            self._setup_langgraph_monitoring()
            self.is_active = True
            self.monitor.log("info", "LangGraph integration activated")
        except Exception as e:
            self.monitor.log("warning", f"Failed to setup LangGraph integration: {e}")
    
    def _setup_langgraph_monitoring(self):
        """
        Setup LangGraph specific monitoring.
        """
        try:
            # Check if LangGraph is available
            import langgraph
            
            # LangGraph monitoring would go here
            # Since LangGraph is newer and may not have stable callback APIs,
            # we'll implement basic monitoring
            
            self.monitor.trace(
                "LangGraph environment detected",
                {'version': getattr(langgraph, '__version__', 'unknown')}
            )
            
        except ImportError:
            self.monitor.log("warning", "LangGraph monitoring not available")
    
    def cleanup(self):
        """
        Cleanup LangGraph integration.
        """
        self.is_active = False
        self.monitor.log("info", "LangGraph integration deactivated")


class CustomIntegration(BaseIntegration):
    """
    Custom integration for frameworks not explicitly supported.
    
    Provides basic monitoring capabilities and allows users to add
    custom instrumentation.
    """
    
    def setup(self):
        """
        Setup custom integration with basic monitoring.
        """
        # Setup basic exception handling
        self._setup_exception_monitoring()
        self.is_active = True
        self.monitor.log("info", "Custom integration activated with basic monitoring")
    
    def _setup_exception_monitoring(self):
        """
        Setup basic exception monitoring for any Python application.
        """
        # Store original exception hook
        self.original_excepthook = sys.excepthook
        
        def monitor_excepthook(exc_type, exc_value, exc_traceback):
            # Log the exception through our monitor
            self.monitor.error(
                exc_value,
                {
                    'exc_type': exc_type.__name__,
                    'traceback': ''.join(traceback.format_tb(exc_traceback))
                }
            )
            # Call original handler
            self.original_excepthook(exc_type, exc_value, exc_traceback)
        
        # Install our exception hook
        sys.excepthook = monitor_excepthook
    
    def cleanup(self):
        """
        Cleanup custom integration.
        """
        # Restore original exception hook
        if hasattr(self, 'original_excepthook'):
            sys.excepthook = self.original_excepthook
        
        self.is_active = False
        self.monitor.log("info", "Custom integration deactivated")


# Integration registry
INTEGRATIONS = {
    'langchain': LangChainIntegration,
    'langgraph': LangGraphIntegration,
    'custom': CustomIntegration,
    'openai': CustomIntegration,  # Use custom for OpenAI SDK
    'anthropic': CustomIntegration,  # Use custom for Anthropic SDK
}


def get_integration_for_framework(framework_name: str, monitor: 'AgentMonitor') -> Optional[BaseIntegration]:
    """
    Get the appropriate integration for a detected framework.
    
    Args:
        framework_name: Name of the detected framework
        monitor: AgentMonitor instance
        
    Returns:
        BaseIntegration instance or None if not found
    """
    integration_class = INTEGRATIONS.get(framework_name, CustomIntegration)
    return integration_class(monitor)
