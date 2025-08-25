"""
Configuration management for agent-monitor package

Handles package-level configuration including API keys, dashboard URLs,
and framework integration settings.
"""

import os
from typing import Dict, Any, Optional


class Config:
    """
    Configuration manager for agent-monitor package.
    """
    
    def __init__(self):
        self.api_key: Optional[str] = None
        self.dashboard_url: Optional[str] = None
        self.timeout: int = 30
        self.retry_count: int = 3
        self.enable_logging: bool = False
        self.framework_config: Dict[str, Any] = {}
        self.auto_detect_frameworks: bool = True
        self._initialized: bool = False
    
    def init(
        self,
        api_key: str,
        dashboard_url: str,
        timeout: int = 30,
        retry_count: int = 3,
        enable_logging: bool = False,
        framework_config: Dict[str, Any] = None,
        auto_detect_frameworks: bool = True
    ):
        """
        Initialize the configuration.
        
        Args:
            api_key: API key for dashboard authentication
            dashboard_url: URL of the monitoring dashboard
            timeout: Request timeout in seconds
            retry_count: Number of retry attempts for failed requests
            enable_logging: Whether to enable debug logging
            framework_config: Framework-specific configuration
            auto_detect_frameworks: Whether to automatically detect and integrate frameworks
        """
        self.api_key = api_key
        self.dashboard_url = dashboard_url
        self.timeout = timeout
        self.retry_count = retry_count
        self.enable_logging = enable_logging
        self.framework_config = framework_config or {}
        self.auto_detect_frameworks = auto_detect_frameworks
        self._initialized = True
    
    def is_initialized(self) -> bool:
        """
        Check if the configuration has been initialized.
        
        Returns:
            bool: True if initialized, False otherwise
        """
        return self._initialized
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        return getattr(self, key, default)
    
    def set(self, key: str, value: Any):
        """
        Set a configuration value.
        
        Args:
            key: Configuration key
            value: Value to set
        """
        setattr(self, key, value)
    
    def update(self, **kwargs):
        """
        Update multiple configuration values.
        
        Args:
            **kwargs: Key-value pairs to update
        """
        for key, value in kwargs.items():
            self.set(key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.
        
        Returns:
            Dict containing all configuration values
        """
        return {
            'api_key': self.api_key,
            'dashboard_url': self.dashboard_url,
            'timeout': self.timeout,
            'retry_count': self.retry_count,
            'enable_logging': self.enable_logging,
            'framework_config': self.framework_config,
            'auto_detect_frameworks': self.auto_detect_frameworks,
            'initialized': self._initialized
        }


# Global configuration instance
_global_config = Config()


def get_config() -> Config:
    """
    Get the global configuration instance.
    
    Returns:
        Config: Global configuration instance
    """
    return _global_config


def init(
    api_key: str,
    dashboard_url: str,
    timeout: int = 30,
    retry_count: int = 3,
    enable_logging: bool = False,
    framework_config: Dict[str, Any] = None
):
    """
    Initialize the global configuration.
    
    Args:
        api_key: API key for dashboard authentication
        dashboard_url: URL of the monitoring dashboard
        timeout: Request timeout in seconds
        retry_count: Number of retry attempts
        enable_logging: Whether to enable debug logging
        framework_config: Framework-specific configuration
    """
    _global_config.init(
        api_key=api_key,
        dashboard_url=dashboard_url,
        timeout=timeout,
        retry_count=retry_count,
        enable_logging=enable_logging,
        framework_config=framework_config
    )
    
    # Auto-setup framework integrations if enabled
    if _global_config.auto_detect_frameworks:
        try:
            from .frameworks import auto_setup_integrations
            auto_setup_integrations()
        except ImportError:
            pass  # Framework integrations not available


def is_initialized() -> bool:
    """
    Check if the global configuration is initialized.
    
    Returns:
        bool: True if initialized, False otherwise
    """
    return _global_config.is_initialized()