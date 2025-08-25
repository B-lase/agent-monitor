# Contributing to Agent Monitor

Thank you for your interest in contributing to Agent Monitor! This document provides guidelines and information for contributors.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Code Style](#code-style)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment tool (venv, conda, etc.)

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/agent-monitor.git
   cd agent-monitor
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Development Dependencies**
   ```bash
   pip install -e ".[dev,all]"
   ```

4. **Verify Installation**
   ```bash
   python -m pytest tests/
   agent-monitor --version
   ```

## Contributing Guidelines

### Types of Contributions

We welcome several types of contributions:

- **Bug Reports**: Help us identify and fix issues
- **Feature Requests**: Suggest new features or improvements
- **Code Contributions**: Submit bug fixes, features, or improvements
- **Documentation**: Improve documentation, examples, or tutorials
- **Testing**: Add test cases or improve test coverage

### Before You Start

1. **Check Existing Issues**: Look through existing issues to avoid duplicates
2. **Discuss Major Changes**: For significant features, open an issue first to discuss
3. **Follow Conventions**: Maintain consistency with existing code style and patterns

## Code Style

### Python Code Standards

- **PEP 8**: Follow Python PEP 8 style guidelines
- **Type Hints**: Use type hints for function signatures and class attributes
- **Docstrings**: Write comprehensive docstrings for all public functions and classes
- **Imports**: Organize imports (standard library, third-party, local)

### Code Formatting

We use automated code formatting:

```bash
# Format code with black
black agent_monitor/ examples/ tests/

# Check with flake8
flake8 agent_monitor/ examples/ tests/
```

### Example Code Style

```python
from typing import Optional, Dict, Any

def example_function(
    agent_id: str,
    metadata: Optional[Dict[str, Any]] = None
) -> bool:
    """
    Example function demonstrating code style.
    
    Args:
        agent_id: Unique identifier for the agent
        metadata: Optional metadata dictionary
        
    Returns:
        bool: True if successful, False otherwise
        
    Raises:
        ValueError: If agent_id is empty
    """
    if not agent_id:
        raise ValueError("agent_id cannot be empty")
        
    # Implementation here
    return True
```

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=agent_monitor

# Run specific test file
python -m pytest tests/test_monitor.py

# Run tests with verbose output
python -m pytest -v
```

### Writing Tests

- Write tests for all new functionality
- Use descriptive test names
- Include both positive and negative test cases
- Mock external dependencies

### Test Structure

```python
import pytest
from unittest.mock import Mock, patch

from agent_monitor import AgentMonitor

class TestAgentMonitor:
    def test_initialization_with_valid_parameters(self):
        """Test that AgentMonitor initializes correctly with valid parameters."""
        monitor = AgentMonitor(
            dashboard_url="https://example.com",
            api_key="test-key"
        )
        assert monitor.dashboard_url == "https://example.com"
        assert monitor.api_key == "test-key"
    
    def test_initialization_without_required_parameters(self):
        """Test that AgentMonitor raises error without required parameters."""
        with pytest.raises(ValueError):
            AgentMonitor(dashboard_url=None, api_key=None)
```

## Submitting Changes

### Pull Request Process

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Write code following our style guidelines
   - Add tests for new functionality
   - Update documentation if needed

3. **Test Changes**
   ```bash
   python -m pytest
   black agent_monitor/ examples/ tests/
   flake8 agent_monitor/ examples/ tests/
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "Add: Brief description of changes"
   ```

5. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Format

Use clear, descriptive commit messages:

```
Add: Brief description of what was added
Fix: Brief description of what was fixed
Update: Brief description of what was updated
Remove: Brief description of what was removed
```

### Pull Request Guidelines

- **Clear Title**: Use a descriptive title
- **Description**: Explain what changes were made and why
- **Testing**: Describe how the changes were tested
- **Documentation**: Update relevant documentation
- **Small PRs**: Keep pull requests focused and reasonably sized

## Reporting Issues

### Bug Reports

When reporting bugs, please include:

- **Description**: Clear description of the issue
- **Steps to Reproduce**: Detailed steps to reproduce the bug
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened
- **Environment**: Python version, OS, package versions
- **Code Sample**: Minimal code example that reproduces the issue

### Feature Requests

For feature requests, please provide:

- **Use Case**: Describe the problem you're trying to solve
- **Proposed Solution**: Your ideas for how to solve it
- **Alternatives**: Other solutions you've considered
- **Additional Context**: Any other relevant information

## Framework Integration Guidelines

### Adding New Framework Support

To add support for a new AI framework:

1. **Create Integration Module**
   - Add new file in `agent_monitor/frameworks/`
   - Follow existing pattern from LangChain/LangGraph integrations

2. **Implement Detection**
   - Add detection logic in `detectors.py`
   - Include version detection and module checking

3. **Add Integration Class**
   - Extend `BaseIntegration`
   - Implement `setup()` and `cleanup()` methods
   - Add framework-specific monitoring hooks

4. **Update Documentation**
   - Add framework to README
   - Include usage examples
   - Document any special configuration

5. **Add Tests**
   - Write tests for detection logic
   - Test integration setup and cleanup
   - Mock framework dependencies

## Questions or Help

If you need help or have questions:

- **GitHub Issues**: Open an issue for bugs or feature requests
- **Discussions**: Use GitHub Discussions for general questions
- **Email**: Contact the maintainers at support@minimax.com

Thank you for contributing to Agent Monitor!