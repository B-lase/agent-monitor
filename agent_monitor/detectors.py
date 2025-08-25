"""
Framework Detection - Automatically detect AI agent frameworks

Provides automatic detection of popular AI frameworks like LangChain, LangGraph,
and others to enable zero-configuration monitoring setup.
"""

import sys
import importlib
from typing import Optional, Dict, Any, List


def detect_framework() -> Dict[str, Any]:
    """
    Automatically detect which AI framework is being used.
    
    Returns:
        Dict containing framework information:
        - name: Framework name ('langchain', 'langgraph', 'custom', etc.)
        - version: Framework version if available
        - available: Whether the framework is importable
        - modules: List of detected framework modules
    """
    detected_frameworks = []
    
    # Check for LangChain
    langchain_info = _check_langchain()
    if langchain_info['available']:
        detected_frameworks.append(langchain_info)
    
    # Check for LangGraph 
    langgraph_info = _check_langgraph()
    if langgraph_info['available']:
        detected_frameworks.append(langgraph_info)
    
    # Check for other frameworks
    openai_info = _check_openai()
    if openai_info['available']:
        detected_frameworks.append(openai_info)
    
    anthropic_info = _check_anthropic()
    if anthropic_info['available']:
        detected_frameworks.append(anthropic_info)
    
    if not detected_frameworks:
        return {
            'name': 'custom',
            'version': None,
            'available': True,
            'modules': [],
            'description': 'Custom or undetected framework'
        }
    
    # Return the most comprehensive framework detected
    primary_framework = max(detected_frameworks, key=lambda f: len(f.get('modules', [])))
    primary_framework['all_detected'] = detected_frameworks
    
    return primary_framework


def _check_langchain() -> Dict[str, Any]:
    """
    Check for LangChain framework availability.
    """
    modules = []
    version = None
    
    try:
        import langchain
        version = getattr(langchain, '__version__', None)
        modules.append('langchain')
        
        # Check for specific LangChain modules
        submodules = [
            'langchain.agents',
            'langchain.chains', 
            'langchain.llms',
            'langchain.chat_models',
            'langchain.embeddings',
            'langchain.vectorstores',
            'langchain.memory',
            'langchain.tools'
        ]
        
        for module in submodules:
            try:
                importlib.import_module(module)
                modules.append(module)
            except ImportError:
                pass
        
        return {
            'name': 'langchain',
            'version': version,
            'available': True,
            'modules': modules,
            'description': 'LangChain framework detected'
        }
        
    except ImportError:
        return {
            'name': 'langchain',
            'version': None,
            'available': False,
            'modules': [],
            'description': 'LangChain not available'
        }


def _check_langgraph() -> Dict[str, Any]:
    """
    Check for LangGraph framework availability.
    """
    modules = []
    version = None
    
    try:
        import langgraph
        version = getattr(langgraph, '__version__', None)
        modules.append('langgraph')
        
        # Check for specific LangGraph modules
        submodules = [
            'langgraph.graph',
            'langgraph.prebuilt',
            'langgraph.checkpoint'
        ]
        
        for module in submodules:
            try:
                importlib.import_module(module)
                modules.append(module)
            except ImportError:
                pass
        
        return {
            'name': 'langgraph',
            'version': version,
            'available': True,
            'modules': modules,
            'description': 'LangGraph framework detected'
        }
        
    except ImportError:
        return {
            'name': 'langgraph',
            'version': None,
            'available': False,
            'modules': [],
            'description': 'LangGraph not available'
        }


def _check_openai() -> Dict[str, Any]:
    """
    Check for OpenAI SDK availability.
    """
    try:
        import openai
        version = getattr(openai, '__version__', None)
        
        return {
            'name': 'openai',
            'version': version,
            'available': True,
            'modules': ['openai'],
            'description': 'OpenAI SDK detected'
        }
        
    except ImportError:
        return {
            'name': 'openai',
            'version': None,
            'available': False,
            'modules': [],
            'description': 'OpenAI SDK not available'
        }


def _check_anthropic() -> Dict[str, Any]:
    """
    Check for Anthropic SDK availability.
    """
    try:
        import anthropic
        version = getattr(anthropic, '__version__', None)
        
        return {
            'name': 'anthropic',
            'version': version,
            'available': True,
            'modules': ['anthropic'],
            'description': 'Anthropic SDK detected'
        }
        
    except ImportError:
        return {
            'name': 'anthropic',
            'version': None,
            'available': False,
            'modules': [],
            'description': 'Anthropic SDK not available'
        }


def get_python_info() -> Dict[str, Any]:
    """
    Get information about the Python environment.
    
    Returns:
        Dict containing Python environment info
    """
    return {
        'version': sys.version,
        'version_info': {
            'major': sys.version_info.major,
            'minor': sys.version_info.minor,
            'micro': sys.version_info.micro
        },
        'executable': sys.executable,
        'platform': sys.platform,
        'modules': list(sys.modules.keys())
    }


def get_environment_info() -> Dict[str, Any]:
    """
    Get comprehensive environment information.
    
    Returns:
        Dict containing complete environment details
    """
    framework_info = detect_framework()
    python_info = get_python_info()
    
    return {
        'framework': framework_info,
        'python': python_info,
        'detected_at': sys.modules.get('time', __import__('time')).time()
    }
