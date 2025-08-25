#!/usr/bin/env python3
"""
LangGraph Framework Integration

This module provides automatic monitoring integration for LangGraph workflows.
When agent-monitor is initialized, it automatically detects and integrates with
LangGraph to provide seamless monitoring of graph execution.
"""

import time
import inspect
from typing import Any, Dict, Optional, Callable
from functools import wraps

try:
    # Try to import LangGraph components
    from langgraph import StateGraph
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False
    StateGraph = None

from ..config import get_config

# Import AgentMonitor with TYPE_CHECKING to avoid circular imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..monitor import AgentMonitor

class LangGraphMonitoringMixin:
    """Mixin class to add monitoring capabilities to LangGraph components"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._monitor: Optional['AgentMonitor'] = None
        self._monitoring_enabled = False
        self._execution_context = {}
        
    def _get_or_create_monitor(self) -> Optional['AgentMonitor']:
        """Get or create a monitor instance for this graph"""
        if not self._monitor and get_config().is_initialized():
            try:
                # Create a monitor for this graph instance
                graph_id = getattr(self, '_graph_id', f"langgraph_{id(self)}")
                graph_name = getattr(self, '_graph_name', "LangGraph Workflow")
                
                self._monitor = AgentMonitor(
                    agent_id=graph_id,
                    agent_name=graph_name,
                    agent_type="langgraph_workflow",
                    metadata={
                        "framework": "langgraph",
                        "auto_detected": True,
                        "node_count": len(getattr(self, 'nodes', {})),
                        "edge_count": len(getattr(self, 'edges', []))
                    }
                )
                self._monitoring_enabled = True
                
            except Exception as e:
                print(f"Warning: Could not create LangGraph monitor: {e}")
                
        return self._monitor
        
    def _log_graph_event(self, event_type: str, data: Dict[str, Any]):
        """Log a graph-level event"""
        monitor = self._get_or_create_monitor()
        if monitor:
            try:
                monitor.log_event(event_type, data)
            except Exception as e:
                print(f"Warning: Failed to log LangGraph event: {e}")
                
    def _log_graph_metric(self, metric_name: str, value: float, unit: str = None):
        """Log a graph-level metric"""
        monitor = self._get_or_create_monitor()
        if monitor:
            try:
                monitor.log_metric(metric_name, value, unit)
            except Exception as e:
                print(f"Warning: Failed to log LangGraph metric: {e}")

def create_monitored_node(original_func: Callable, node_name: str) -> Callable:
    """Create a monitored version of a node function"""
    
    @wraps(original_func)
    def monitored_node(state: Any, *args, **kwargs) -> Any:
        # Get the graph instance from the call stack
        graph_instance = None
        for frame_info in inspect.stack():
            frame_locals = frame_info.frame.f_locals
            if 'self' in frame_locals and hasattr(frame_locals['self'], '_get_or_create_monitor'):
                graph_instance = frame_locals['self']
                break
                
        if graph_instance:
            monitor = graph_instance._get_or_create_monitor()
            if monitor:
                start_time = time.time()
                
                # Log node execution start
                monitor.log_event("node_execution_start", {
                    "node_name": node_name,
                    "input_state_keys": list(state.keys()) if isinstance(state, dict) else "non_dict_state",
                    "timestamp": start_time
                })
                
                try:
                    # Execute the original node function
                    result = original_func(state, *args, **kwargs)
                    
                    execution_time = time.time() - start_time
                    
                    # Log successful execution
                    monitor.log_event("node_execution_complete", {
                        "node_name": node_name,
                        "execution_time": execution_time,
                        "output_state_keys": list(result.keys()) if isinstance(result, dict) else "non_dict_state",
                        "status": "success"
                    })
                    
                    # Log performance metrics
                    monitor.log_metric(f"node_{node_name}_duration", execution_time, "seconds")
                    
                    return result
                    
                except Exception as e:
                    execution_time = time.time() - start_time
                    
                    # Log node execution error
                    monitor.log_event("node_execution_error", {
                        "node_name": node_name,
                        "execution_time": execution_time,
                        "error_type": type(e).__name__,
                        "error_message": str(e),
                        "status": "error"
                    })
                    
                    raise  # Re-raise the original exception
        
        # Fallback: execute without monitoring
        return original_func(state, *args, **kwargs)
        
    return monitored_node

if LANGGRAPH_AVAILABLE:
    class MonitoredStateGraph(LangGraphMonitoringMixin, StateGraph):
        """Enhanced StateGraph with automatic monitoring"""
        
        def __init__(self, state_schema, graph_id: str = None, graph_name: str = None):
            # Set graph identification
            self._graph_id = graph_id or f"langgraph_{int(time.time())}"
            self._graph_name = graph_name or "LangGraph Workflow"
            
            # Initialize parent classes
            super().__init__(state_schema)
            
            # Override the original nodes dict to monitor additions
            self._original_nodes = self.nodes
            
        def add_node(self, name: str, func: Callable):
            """Override add_node to add monitoring"""
            # Wrap the function with monitoring
            monitored_func = create_monitored_node(func, name)
            
            # Call the original add_node with the monitored function
            result = super().add_node(name, monitored_func)
            
            # Log node addition
            self._log_graph_event("node_added", {
                "node_name": name,
                "function_name": func.__name__,
                "total_nodes": len(self.nodes)
            })
            
            return result
            
        def add_edge(self, from_node: str, to_node: str):
            """Override add_edge to add monitoring"""
            result = super().add_edge(from_node, to_node)
            
            # Log edge addition
            self._log_graph_event("edge_added", {
                "from_node": from_node,
                "to_node": to_node,
                "total_edges": len(getattr(self, 'edges', []))
            })
            
            return result
            
        def compile(self, **kwargs):
            """Override compile to add monitoring"""
            start_time = time.time()
            
            # Log compilation start
            self._log_graph_event("graph_compilation_start", {
                "node_count": len(self.nodes),
                "edge_count": len(getattr(self, 'edges', [])),
                "compilation_options": kwargs
            })
            
            try:
                # Compile the graph
                compiled_graph = super().compile(**kwargs)
                
                compilation_time = time.time() - start_time
                
                # Log successful compilation
                self._log_graph_event("graph_compilation_complete", {
                    "compilation_time": compilation_time,
                    "status": "success"
                })
                
                self._log_graph_metric("compilation_time", compilation_time, "seconds")
                
                # Return a monitored version of the compiled graph
                return MonitoredCompiledGraph(compiled_graph, self._monitor)
                
            except Exception as e:
                compilation_time = time.time() - start_time
                
                # Log compilation error
                self._log_graph_event("graph_compilation_error", {
                    "compilation_time": compilation_time,
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "status": "error"
                })
                
                raise  # Re-raise the original exception
    
    class MonitoredCompiledGraph:
        """Wrapper for compiled LangGraph with monitoring"""
        
        def __init__(self, compiled_graph, monitor: Optional['AgentMonitor']):
            self._compiled_graph = compiled_graph
            self._monitor = monitor
            
        def invoke(self, input_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
            """Execute the graph with monitoring"""
            if self._monitor:
                self._monitor.start_session()
                
                start_time = time.time()
                
                # Log invocation start
                self._monitor.log_event("graph_invocation_start", {
                    "input_keys": list(input_data.keys()) if isinstance(input_data, dict) else "non_dict_input",
                    "invocation_options": kwargs,
                    "timestamp": start_time
                })
                
                self._monitor.update_status("running")
                
                try:
                    # Execute the compiled graph
                    result = self._compiled_graph.invoke(input_data, **kwargs)
                    
                    execution_time = time.time() - start_time
                    
                    # Log successful execution
                    self._monitor.log_event("graph_invocation_complete", {
                        "execution_time": execution_time,
                        "output_keys": list(result.keys()) if isinstance(result, dict) else "non_dict_output",
                        "status": "success"
                    })
                    
                    self._monitor.log_metric("graph_execution_time", execution_time, "seconds")
                    self._monitor.update_status("completed")
                    
                    self._monitor.end_session()
                    
                    return result
                    
                except Exception as e:
                    execution_time = time.time() - start_time
                    
                    # Log execution error
                    self._monitor.log_event("graph_invocation_error", {
                        "execution_time": execution_time,
                        "error_type": type(e).__name__,
                        "error_message": str(e),
                        "status": "error"
                    })
                    
                    self._monitor.update_status("error")
                    self._monitor.end_session()
                    
                    raise  # Re-raise the original exception
            else:
                # Execute without monitoring
                return self._compiled_graph.invoke(input_data, **kwargs)
                
        def __getattr__(self, name):
            """Delegate other methods to the compiled graph"""
            return getattr(self._compiled_graph, name)

    # Monkey patch the original StateGraph class
    def patch_langgraph():
        """Apply monitoring patches to LangGraph"""
        try:
            import langgraph
            # Replace StateGraph with MonitoredStateGraph
            langgraph.StateGraph = MonitoredStateGraph
            return True
        except Exception as e:
            print(f"Warning: Could not patch LangGraph: {e}")
            return False
else:
    # LangGraph not available - provide mock implementations
    class MonitoredStateGraph:
        def __init__(self, *args, **kwargs):
            raise ImportError("LangGraph is not installed. Install it with: pip install langgraph")
    
    def patch_langgraph():
        print("Warning: LangGraph is not available for patching")
        return False

def setup_langgraph_monitoring():
    """Set up LangGraph monitoring integration"""
    if not LANGGRAPH_AVAILABLE:
        return False
        
    config = get_config()
    if not config.is_initialized():
        return False
        
    # Get framework configuration
    framework_config = config.framework_config.get('langgraph', {})
    
    if framework_config.get('auto_patch', True):
        success = patch_langgraph()
        if success:
            print("LangGraph monitoring integration enabled")
        return success
    
    return True

# Auto-setup when module is imported
if LANGGRAPH_AVAILABLE and get_config().is_initialized():
    setup_langgraph_monitoring()