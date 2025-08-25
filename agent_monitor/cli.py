#!/usr/bin/env python3
"""
Command Line Interface for Agent Monitor

Provides CLI commands for managing agent monitoring, testing connections,
and viewing status information.
"""

import argparse
import sys
import time
from typing import Optional

from . import AgentMonitor
from .detectors import detect_framework, get_environment_info
from .config import get_config


def cmd_test_connection(args):
    """Test connection to the dashboard API"""
    print("Testing connection to dashboard...")
    
    try:
        monitor = AgentMonitor(
            dashboard_url=args.dashboard_url,
            api_key=args.api_key,
            agent_name="cli-test-agent",
            auto_detect=False
        )
        
        agent_id = monitor.start()
        print(f"✅ Connection successful! Agent ID: {agent_id}")
        
        # Test logging
        monitor.log("info", "CLI connection test successful")
        print("✅ Logging test successful")
        
        # Test status update
        monitor.update_status("idle")
        print("✅ Status update successful")
        
        time.sleep(1)
        monitor.stop()
        print("✅ All tests passed!")
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return 1
    
    return 0


def cmd_detect_frameworks(args):
    """Detect available AI frameworks"""
    print("Detecting AI frameworks...\n")
    
    framework_info = detect_framework()
    env_info = get_environment_info()
    
    print(f"Primary Framework: {framework_info.get('name', 'unknown')}")
    print(f"Version: {framework_info.get('version', 'unknown')}")
    print(f"Available: {framework_info.get('available', False)}")
    print(f"Description: {framework_info.get('description', 'N/A')}")
    
    if framework_info.get('modules'):
        print(f"\nDetected Modules:")
        for module in framework_info['modules']:
            print(f"  - {module}")
    
    # Show all detected frameworks
    if 'all_detected' in framework_info:
        print(f"\nAll Detected Frameworks:")
        for fw in framework_info['all_detected']:
            status = "✅" if fw.get('available') else "❌"
            print(f"  {status} {fw.get('name', 'unknown')} - {fw.get('description', 'N/A')}")
    
    print(f"\nPython Version: {env_info['python']['version_info']['major']}.{env_info['python']['version_info']['minor']}.{env_info['python']['version_info']['micro']}")
    print(f"Platform: {env_info['python']['platform']}")
    
    return 0


def cmd_start_monitoring(args):
    """Start interactive monitoring session"""
    print(f"Starting agent monitoring session...")
    print(f"Dashboard: {args.dashboard_url}")
    print(f"Agent: {args.agent_name or 'auto-generated'}")
    print(f"Group: {args.group_id}")
    print("\nPress Ctrl+C to stop monitoring\n")
    
    try:
        monitor = AgentMonitor(
            dashboard_url=args.dashboard_url,
            api_key=args.api_key,
            agent_name=args.agent_name,
            group_id=args.group_id,
            auto_detect=not args.no_auto_detect
        )
        
        agent_id = monitor.start()
        print(f"✅ Agent monitoring started! ID: {agent_id}")
        
        # Send some test events
        monitor.log("info", "Agent monitoring session started via CLI")
        monitor.update_status("running")
        
        # Keep running until interrupted
        try:
            while True:
                time.sleep(10)
                monitor.log("debug", f"Heartbeat at {time.time()}")
        except KeyboardInterrupt:
            print("\n🛑 Stopping monitoring...")
            monitor.update_status("offline")
            monitor.stop()
            print("✅ Monitoring stopped successfully")
            
    except Exception as e:
        print(f"❌ Failed to start monitoring: {e}")
        return 1
    
    return 0


def cmd_version(args):
    """Show version information"""
    from . import __version__, __author__
    
    print(f"Agent Monitor v{__version__}")
    print(f"Author: {__author__}")
    print(f"Python: {sys.version.split()[0]}")
    
    return 0


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Agent Monitor CLI - Monitor AI agents in real-time",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test connection to dashboard
  agent-monitor test --dashboard-url https://dashboard.com --api-key your-key
  
  # Detect available frameworks
  agent-monitor detect
  
  # Start interactive monitoring
  agent-monitor start --dashboard-url https://dashboard.com --api-key your-key
  
  # Start with custom agent name
  agent-monitor start --dashboard-url https://dashboard.com --api-key your-key --agent-name my-agent
        """
    )
    
    parser.add_argument(
        "--version", 
        action="store_true",
        help="Show version information"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Test command
    test_parser = subparsers.add_parser("test", help="Test connection to dashboard")
    test_parser.add_argument("--dashboard-url", required=True, help="Dashboard URL")
    test_parser.add_argument("--api-key", required=True, help="API key")
    test_parser.set_defaults(func=cmd_test_connection)
    
    # Detect command
    detect_parser = subparsers.add_parser("detect", help="Detect available AI frameworks")
    detect_parser.set_defaults(func=cmd_detect_frameworks)
    
    # Start command
    start_parser = subparsers.add_parser("start", help="Start interactive monitoring session")
    start_parser.add_argument("--dashboard-url", required=True, help="Dashboard URL")
    start_parser.add_argument("--api-key", required=True, help="API key")
    start_parser.add_argument("--agent-name", help="Agent name (auto-generated if not provided)")
    start_parser.add_argument("--group-id", default="default", help="Group ID for organizing agents")
    start_parser.add_argument("--no-auto-detect", action="store_true", help="Disable automatic framework detection")
    start_parser.set_defaults(func=cmd_start_monitoring)
    
    # Version command
    version_parser = subparsers.add_parser("version", help="Show version information")
    version_parser.set_defaults(func=cmd_version)
    
    args = parser.parse_args()
    
    # Handle version flag
    if args.version:
        return cmd_version(args)
    
    # Handle no command
    if not args.command:
        parser.print_help()
        return 1
    
    # Execute command
    try:
        return args.func(args)
    except Exception as e:
        print(f"❌ Command failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())