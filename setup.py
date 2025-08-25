from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="agent-monitor",
    version="1.0.0",
    author="MiniMax",
    author_email="support@minimax.com",
    description="A real-time monitoring package for AI agents with dashboard integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/minimax/agent-monitor",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "psutil>=5.8.0",  # For performance monitoring examples
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-asyncio",
            "black",
            "flake8",
        ],
        "langchain": ["langchain>=0.1.0", "langchain-core>=0.1.0"],
        "langgraph": ["langgraph>=0.1.0"],
        "openai": ["openai>=1.0.0"],
        "anthropic": ["anthropic>=0.8.0"],
        "performance": ["psutil>=5.8.0"],
        "all": [
            "langchain>=0.1.0",
            "langchain-core>=0.1.0",
            "langgraph>=0.1.0",
            "openai>=1.0.0",
            "anthropic>=0.8.0",
            "psutil>=5.8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "agent-monitor=agent_monitor.cli:main",
        ],
    },
)
