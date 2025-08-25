#!/usr/bin/env python3
"""
LangChain Framework Integration

This module provides automatic monitoring integration for LangChain agents and chains.
When agent-monitor is initialized, it automatically detects and integrates with
LangChain to provide seamless monitoring of agent decisions and tool usage.
"""

import time
import inspect
from typing import Any, Dict, Optional, Callable, List
from functools import wraps

try:
    # Try to import LangChain components
    from langchain.agents import BaseMultiActionAgent, BaseSingleActionAgent
    from langchain.chains.base import Chain
    from langchain.tools.base import BaseTool
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    BaseMultiActionAgent = None
    BaseSingleActionAgent = None
    Chain = None
    BaseTool = None

from ..config import get_config

# Import AgentMonitor with TYPE_CHECKING to avoid circular imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..monitor import AgentMonitor

class LangChainMonitoringMixin:
    """Mixin class to add monitoring capabilities to LangChain components"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._monitor: Optional['AgentMonitor'] = None
        self._monitoring_enabled = False
        
    def _get_or_create_monitor(self) -> Optional['AgentMonitor']:
        """Get or create a monitor instance for this component"""
        if not self._monitor and get_config().is_initialized():
            try:
                # Create a monitor for this component
                component_id = getattr(self, '_component_id', f"langchain_{type(self).__name__}_{id(self)}")
                component_name = getattr(self, '_component_name', f"LangChain {type(self).__name__}")
                
                self._monitor = AgentMonitor(
                    agent_id=component_id,
                    agent_name=component_name,
                    agent_type="langchain_component",
                    metadata={
                        "framework": "langchain",
                        "component_type": type(self).__name__,
                        "auto_detected": True
                    }
                )
                self._monitoring_enabled = True
                
            except Exception as e:
                print(f"Warning: Could not create LangChain monitor: {e}")
                
        return self._monitor
        
    def _log_component_event(self, event_type: str, data: Dict[str, Any]):
        """Log a component-level event"""
        monitor = self._get_or_create_monitor()
        if monitor:
            try:
                monitor.log_event(event_type, data)
            except Exception as e:
                print(f"Warning: Failed to log LangChain event: {e}")
                
    def _log_component_metric(self, metric_name: str, value: float, unit: str = None):
        """Log a component-level metric"""
        monitor = self._get_or_create_monitor()
        if monitor:
            try:
                monitor.log_metric(metric_name, value, unit)
            except Exception as e:
                print(f"Warning: Failed to log LangChain metric: {e}")

if LANGCHAIN_AVAILABLE:
    class MonitoredAgent(LangChainMonitoringMixin):
        """Base class for monitored LangChain agents"""
        
        def plan(self, intermediate_steps, **kwargs):
            """Override plan method to add monitoring"""
            start_time = time.time()
            
            # Log planning start
            self._log_component_event("agent_planning_start", {
                "intermediate_steps_count": len(intermediate_steps),
                "planning_context": kwargs
            })
            
            try:
                # Execute original planning
                result = super().plan(intermediate_steps, **kwargs)
                
                planning_time = time.time() - start_time
                
                # Log successful planning
                self._log_component_event("agent_planning_complete", {
                    "planning_time": planning_time,
                    "action_count": len(result) if isinstance(result, list) else 1,
                    "status": "success"
                })
                
                self._log_component_metric("planning_time", planning_time, "seconds")
                
                return result
                
            except Exception as e:
                planning_time = time.time() - start_time
                
                # Log planning error
                self._log_component_event("agent_planning_error", {
                    "planning_time": planning_time,
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "status": "error"
                })
                
                raise  # Re-raise the original exception
                
    class MonitoredChain(LangChainMonitoringMixin):
        """Base class for monitored LangChain chains"""
        
        def _call(self, inputs: Dict[str, Any], **kwargs) -> Dict[str, Any]:
            """Override _call method to add monitoring"""
            monitor = self._get_or_create_monitor()
            if monitor:
                monitor.start_session()
                
            start_time = time.time()
            
            # Log chain execution start
            self._log_component_event("chain_execution_start", {
                "input_keys": list(inputs.keys()),
                "chain_type": type(self).__name__,
                "execution_options": kwargs
            })
            
            if monitor:
                monitor.update_status("running")
                
            try:
                # Execute original chain logic
                result = super()._call(inputs, **kwargs)
                
                execution_time = time.time() - start_time
                
                # Log successful execution
                self._log_component_event("chain_execution_complete", {
                    "execution_time": execution_time,
                    "output_keys": list(result.keys()) if isinstance(result, dict) else "non_dict_output",
                    "status": "success"
                })
                
                self._log_component_metric("chain_execution_time", execution_time, "seconds")
                
                if monitor:
                    monitor.update_status("completed")
                    monitor.end_session()
                    
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                
                # Log execution error
                self._log_component_event("chain_execution_error", {
                    "execution_time": execution_time,
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "status": "error"
                })
                
                if monitor:
                    monitor.update_status("error")
                    monitor.end_session()
                    
                raise  # Re-raise the original exception
                
    class MonitoredTool(LangChainMonitoringMixin):
        """Base class for monitored LangChain tools"""
        
        def _run(self, query: str, **kwargs) -> str:
            """Override _run method to add monitoring"""
            start_time = time.time()
            
            # Log tool usage start
            self._log_component_event("tool_usage_start", {
                "tool_name": getattr(self, 'name', type(self).__name__),
                "query_length": len(query),
                "tool_options": kwargs
            })
            
            try:
                # Execute original tool logic
                result = super()._run(query, **kwargs)
                
                execution_time = time.time() - start_time
                
                # Log successful tool usage
                self._log_component_event("tool_usage_complete", {
                    "tool_name": getattr(self, 'name', type(self).__name__),
                    "execution_time": execution_time,
                    "result_length": len(str(result)),
                    "status": "success"
                })
                
                self._log_component_metric(f"tool_{getattr(self, 'name', 'unknown')}_duration", execution_time, "seconds")
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                
                # Log tool usage error
                self._log_component_event("tool_usage_error", {
                    "tool_name": getattr(self, 'name', type(self).__name__),
                    "execution_time": execution_time,
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "status": "error"
                })
                
                raise  # Re-raise the original exception
                
    def create_monitored_agent_executor(original_executor_class):
        """Create a monitored version of an agent executor"""
        
        class MonitoredAgentExecutor(LangChainMonitoringMixin, original_executor_class):
            """Monitored version of AgentExecutor"""
            
            def _call(self, inputs: Dict[str, str], **kwargs) -> Dict[str, Any]:
                """Override _call to monitor agent execution"""
                monitor = self._get_or_create_monitor()
                if monitor:
                    monitor.start_session()
                    
                start_time = time.time()
                intermediate_steps = []
                
                # Log agent execution start
                self._log_component_event("agent_execution_start", {
                    "input_text": inputs.get(self.input_keys[0], ""),
                    "max_iterations": getattr(self, 'max_iterations', None),
                    "available_tools": [tool.name for tool in getattr(self, 'tools', [])]
                })
                
                if monitor:
                    monitor.update_status("running")
                    
                try:
                    # Execute the original agent logic with step monitoring
                    result = self._execute_with_monitoring(inputs, **kwargs)
                    
                    execution_time = time.time() - start_time
                    
                    # Log successful execution
                    self._log_component_event("agent_execution_complete", {
                        "execution_time": execution_time,
                        "total_steps": len(intermediate_steps),
                        "final_answer": result.get(self.output_keys[0], ""),
                        "status": "success"
                    })
                    
                    self._log_component_metric("agent_execution_time", execution_time, "seconds")
                    self._log_component_metric("agent_steps_count", len(intermediate_steps), "steps")
                    
                    if monitor:
                        monitor.update_status("completed")
                        monitor.end_session()
                        
                    return result
                    
                except Exception as e:
                    execution_time = time.time() - start_time
                    
                    # Log execution error
                    self._log_component_event("agent_execution_error", {
                        "execution_time": execution_time,
                        "completed_steps": len(intermediate_steps),
                        "error_type": type(e).__name__,
                        "error_message": str(e),
                        "status": "error"
                    })
                    
                    if monitor:
                        monitor.update_status("error")
                        monitor.end_session()
                        
                    raise  # Re-raise the original exception
                    
            def _execute_with_monitoring(self, inputs: Dict[str, str], **kwargs) -> Dict[str, Any]:
                """Execute agent with step-by-step monitoring"""
                # This would be implemented based on the specific AgentExecutor structure
                # For now, delegate to the original implementation
                return super()._call(inputs, **kwargs)
                
        return MonitoredAgentExecutor
        
    # Monkey patching functions
    def patch_langchain():
        """Apply monitoring patches to LangChain"""
        try:
            import langchain
            
            # Patch common agent types
            if hasattr(langchain, 'agents'):
                if hasattr(langchain.agents, 'AgentExecutor'):
                    original_executor = langchain.agents.AgentExecutor
                    langchain.agents.AgentExecutor = create_monitored_agent_executor(original_executor)
                    
            # Patch chains
            if hasattr(langchain, 'chains'):
                # This would patch various chain types
                pass
                
            # Patch tools
            if hasattr(langchain, 'tools'):
                # This would patch tool base classes
                pass
                
            return True
            
        except Exception as e:
            print(f"Warning: Could not patch LangChain: {e}")
            return False
else:
    # LangChain not available - provide mock implementations
    def patch_langchain():
        print("Warning: LangChain is not available for patching")
        return False

def setup_langchain_monitoring():
    """Set up LangChain monitoring integration"""
    if not LANGCHAIN_AVAILABLE:
        return False
        
    config = get_config()
    if not config.is_initialized():
        return False
        
    # Get framework configuration
    framework_config = config.framework_config.get('langchain', {})
    
    if framework_config.get('auto_patch', True):
        success = patch_langchain()
        if success:
            print("LangChain monitoring integration enabled")
        return success
    
    return True

# Auto-setup when module is imported
if LANGCHAIN_AVAILABLE and get_config().is_initialized():
    setup_langchain_monitoring()