"""
Test script to verify the agent-monitor package works with the dashboard.
"""

import sys
import os

# Add the package to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from agent_monitor import AgentMonitor
from agent_monitor.detectors import detect_framework
from agent_monitor.exceptions import AgentMonitorError

def test_framework_detection():
    """
    Test framework detection functionality.
    """
    print("Testing framework detection...")
    framework_info = detect_framework()
    print(f"Detected framework: {framework_info['name']}")
    print(f"Available: {framework_info['available']}")
    if framework_info.get('version'):
        print(f"Version: {framework_info['version']}")
    print()
    return framework_info

def test_dashboard_connection():
    """
    Test connection to the dashboard.
    """
    print("Testing dashboard connection...")
    
    # Use the known working dashboard URL and the correct API key
    dashboard_url = "https://0f3jus9vnfzq.space.minimax.io"
    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InliaGphYmlyb21zbW5xcnptbmFiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU0NTk0ODcsImV4cCI6MjA3MTAzNTQ4N30.jmWskjMDuU8RsYAvThRQLksuFKru1WgtZ7aAOQtNcyw"
    
    try:
        monitor = AgentMonitor(
            dashboard_url=dashboard_url,
            api_key=api_key,
            agent_name="test_package_agent",
            group_id="package_test"
        )
        
        print("Attempting to register agent...")
        agent_id = monitor.start()
        print(f"SUCCESS: Agent registered with ID: {agent_id}")
        
        # Test logging
        print("Testing log submission...")
        monitor.log("info", "Test message from package verification")
        monitor.log("trace", "Package test trace", {"test": True, "package_version": "1.0.0"})
        
        # Test status update
        print("Testing status update...")
        monitor.update_status("running", {"test_phase": "connection_test"})
        
        print("SUCCESS: All basic functions working!")
        
        # Stop monitoring
        monitor.stop()
        print("Agent stopped successfully.")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    print("Agent Monitor Package Test")
    print("=" * 40)
    
    # Test 1: Framework detection
    framework_info = test_framework_detection()
    
    # Test 2: Dashboard connection
    connection_success = test_dashboard_connection()
    
    # Summary
    print("\nTest Summary:")
    print("=" * 40)
    print(f"Framework Detection: {'PASS' if framework_info else 'FAIL'}")
    print(f"Dashboard Connection: {'PASS' if connection_success else 'FAIL'}")
    
    if connection_success:
        print("\n✓ Package is working correctly!")
        print("✓ Check the dashboard to see the test agent data.")
        return 0
    else:
        print("\n✗ Package test failed.")
        return 1

if __name__ == "__main__":
    exit(main())
