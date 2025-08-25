#!/usr/bin/env python3
"""
Frameworks Package

This package provides automatic monitoring integration for popular AI agent frameworks.
Currently supported:
- LangGraph: Automatic workflow monitoring
- LangChain: Agent and chain execution monitoring

Framework integration is automatically enabled when agent-monitor is initialized
and the respective framework packages are available.
"""

from typing import Dict, Any
from ..config import get_config

# Framework detection and integration
def detect_available_frameworks() -> Dict[str, bool]:
    """Detect which AI frameworks are available in the current environment"""
    frameworks = {
        'langgraph': False,
        'langchain': False,
        'autogen': False,
        'crew': False
    }
    
    # Check LangGraph
    try:
        import langgraph
        frameworks['langgraph'] = True
    except ImportError:
        pass
        
    # Check LangChain
    try:
        import langchain
        frameworks['langchain'] = True
    except ImportError:
        pass
        
    # Check AutoGen
    try:
        import autogen
        frameworks['autogen'] = True
    except ImportError:
        pass
        
    # Check CrewAI
    try:
        import crew
        frameworks['crew'] = True
    except ImportError:
        pass
        
    return frameworks

def setup_framework_integrations(framework_config: Dict[str, Any] = None):
    """Set up automatic monitoring for detected frameworks"""
    if not get_config().is_initialized():
        return False
        
    framework_config = framework_config or {}
    available_frameworks = detect_available_frameworks()
    
    integration_results = {}
    
    # Set up LangGraph integration
    if available_frameworks['langgraph']:
        try:
            from .langgraph import setup_langgraph_monitoring
            integration_results['langgraph'] = setup_langgraph_monitoring()
        except Exception as e:
            print(f"Warning: Failed to set up LangGraph integration: {e}")
            integration_results['langgraph'] = False
            
    # Set up LangChain integration
    if available_frameworks['langchain']:
        try:
            from .langchain import setup_langchain_monitoring
            integration_results['langchain'] = setup_langchain_monitoring()
        except Exception as e:
            print(f"Warning: Failed to set up LangChain integration: {e}")
            integration_results['langchain'] = False
            
    # Future framework integrations can be added here
    
    return integration_results

def get_framework_status():
    """Get the current status of framework integrations"""
    available = detect_available_frameworks()
    config = get_config()
    
    status = {
        'available_frameworks': available,
        'monitoring_initialized': config.is_initialized(),
        'framework_config': config.framework_config if config.is_initialized() else {}
    }
    
    return status

# Auto-detect and setup integrations when the package is initialized
def auto_setup_integrations():
    """Automatically set up integrations for detected frameworks"""
    config = get_config()
    if config.is_initialized() and config.auto_detect_frameworks:
        results = setup_framework_integrations(config.framework_config)
        
        # Report successful integrations
        successful = [fw for fw, success in results.items() if success]
        if successful:
            print(f"Agent monitoring enabled for: {', '.join(successful)}")
            
        return results
    return {}