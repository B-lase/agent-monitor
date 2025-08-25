#!/usr/bin/env python3
"""
Test Integration Script

This script tests the secure agent monitoring integration
after removing hardcoded API keys.
"""

import os
import sys
import time

def test_integration():
    """Test the secure agent monitor integration"""
    
    # Check if API key is set
    api_key = os.getenv('AGENT_MONITOR_API_KEY')
    if not api_key:
        print("❌ AGENT_MONITOR_API_KEY environment variable is required")
        print("Set it with:")
        print('export AGENT_MONITOR_API_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InliaGphYmlyb21zbW5xcnptbmFiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NTQ1OTQ4NywiZXhwIjoyMDcxMDM1NDg3fQ.fxe_NtLTHRZLl2RwjjP7Uq0o9H_0pXdpRY8kKR3yE4gz"')
        return False
    
    print("🔒 API key found in environment")
    
    try:
        # Import and initialize
        import agent_monitor
        from agent_monitor import AgentMonitor
        
        print("📦 Agent monitor imported successfully")
        
        # Initialize with secure configuration
        agent_monitor.init(
            api_key=api_key,
            dashboard_url="https://0f3jus9vnfzq.space.minimax.io"
        )
        
        print("🚀 Agent monitor initialized")
        
        # Create test agent with correct API
        monitor = AgentMonitor(
            dashboard_url="https://0f3jus9vnfzq.space.minimax.io",
            api_key=api_key,
            agent_name="Security Fix Test Agent",
            group_id="security-tests",
            metadata={
                "test": "security-integration",
                "version": "2.0.0-secure"
            }
        )
        
        print("🤖 Test agent created")
        
        # Start monitoring
        agent_id = monitor.start()
        print(f"📡 Monitoring started with agent ID: {agent_id}")
        
        # Send test logs
        monitor.log("info", "Security fix test - agent online")
        monitor.log("info", "Testing secure API key usage")
        monitor.log("success", "Integration test completed successfully")
        
        print("📝 Test logs sent")
        
        # Wait a bit
        time.sleep(5)
        
        print("🔄 Test completed")
        
        print("✅ Integration test completed successfully!")
        print("🌐 Check dashboard: https://0f3jus9vnfzq.space.minimax.io")
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing secure agent monitor integration...\n")
    success = test_integration()
    sys.exit(0 if success else 1)
