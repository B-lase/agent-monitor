"""
Custom exceptions for the agent monitor package.
"""


class AgentMonitorError(Exception):
    """
    Base exception for all agent monitor related errors.
    """
    pass


class ConnectionError(AgentMonitorError):
    """
    Raised when unable to connect to the dashboard API.
    """
    pass


class AuthenticationError(AgentMonitorError):
    """
    Raised when API authentication fails.
    """
    pass


class ConfigurationError(AgentMonitorError):
    """
    Raised when there are configuration issues.
    """
    pass
