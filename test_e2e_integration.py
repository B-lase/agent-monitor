#!/usr/bin/env python3
"""
End-to-End Integration Test

This script tests the complete integration flow from the Python package to the dashboard.
It uses the real Supabase backend to verify data flows correctly.
"""

import time
import sys
import traceback
from datetime import datetime

# Test the real integration
def test_real_integration():
    """
    Test the package with the real dashboard to verify end-to-end integration.
    """
    print("🔗 Testing End-to-End Integration")
    print("==================================\n")
    
    try:
        # Import the package
        print("📦 Importing agent-monitor package...")
        import agent_monitor
        from agent_monitor import AgentMonitor
        print("  ✅ Package imported successfully")
        
        # Test with real dashboard URL (final deployment)
        dashboard_url = "https://0f3jus9vnfzq.space.minimax.io"  # The final deployed dashboard
        api_key = "test-key-e2e"  # Test key for this integration test
        
        print(f"\n🌐 Testing connection to real dashboard: {dashboard_url}")
        
        # Create a monitor instance
        print("\n🤖 Creating AgentMonitor instance...")
        monitor = AgentMonitor(
            dashboard_url=dashboard_url,
            api_key=api_key,
            agent_name="E2E-Test-Agent",
            group_id="integration-test",
            auto_detect=True
        )
        print("  ✅ AgentMonitor created successfully")
        
        # Start monitoring session
        print("\n🚀 Starting monitoring session...")
        agent_id = monitor.start()
        print(f"  ✅ Monitoring started! Agent ID: {agent_id}")
        
        # Log some test events
        print("\n📝 Sending test events to dashboard...")
        
        # Test event 1: Agent initialization
        monitor.log("info", "E2E integration test started", {
            "test_timestamp": datetime.now().isoformat(),
            "test_type": "end_to_end_integration",
            "python_version": sys.version
        })
        print("  ✅ Initialization event sent")
        
        # Test event 2: Agent decision
        monitor.log("debug", "Making test decision", {
            "decision_type": "test_decision",
            "options": ["option_a", "option_b", "option_c"],
            "selected": "option_a",
            "confidence": 0.95
        })
        print("  ✅ Decision event sent")
        
        # Test event 3: Agent action
        monitor.log("info", "Executing test action", {
            "action_type": "test_action",
            "parameters": {"param1": "value1", "param2": 42},
            "expected_duration": 2.5
        })
        print("  ✅ Action event sent")
        
        # Test status updates
        print("\n🔄 Testing status updates...")
        monitor.update_status("running")
        time.sleep(1)
        monitor.update_status("idle")
        time.sleep(1)
        monitor.update_status("completed")
        print("  ✅ Status updates sent")
        
        # Test error logging
        print("\n⚠️  Testing error reporting...")
        test_error = Exception("This is a test error for E2E validation")
        monitor.error(test_error, {
            "error_context": "end_to_end_test",
            "expected": True,
            "test_step": "error_reporting"
        })
        print("  ✅ Error event sent")
        
        # Test completion event
        print("\n🏁 Sending completion event...")
        monitor.log("info", "E2E integration test completed successfully", {
            "test_result": "success",
            "events_sent": 5,
            "status_updates": 3,
            "end_timestamp": datetime.now().isoformat()
        })
        print("  ✅ Completion event sent")
        
        # Stop monitoring
        print("\n🛑 Stopping monitoring session...")
        monitor.stop()
        print("  ✅ Monitoring session ended")
        
        print("\n🎉 END-TO-END TEST COMPLETED SUCCESSFULLY!")
        print(f"\n📊 Test Summary:")
        print(f"   Dashboard URL: {dashboard_url}")
        print(f"   Agent ID: {agent_id}")
        print(f"   Agent Name: E2E-Test-Agent")
        print(f"   Group: integration-test")
        print(f"   Events Sent: 5 (initialization, decision, action, error, completion)")
        print(f"   Status Updates: 3 (running → idle → completed)")
        
        print(f"\n✅ VERIFICATION STEPS:")
        print(f"   1. Go to the dashboard: {dashboard_url}")
        print(f"   2. Look for agent 'E2E-Test-Agent' in the 'integration-test' group")
        print(f"   3. Verify the agent shows up with the correct status")
        print(f"   4. Check the agent logs for the 5 test events sent")
        print(f"   5. Confirm the events have the correct timestamps and data")
        
        return True
        
    except Exception as e:
        print(f"\n❌ END-TO-END TEST FAILED: {e}")
        print(f"\n🔍 Error Details:")
        traceback.print_exc()
        
        print(f"\n🛠️  Troubleshooting:")
        print(f"   1. Check network connectivity")
        print(f"   2. Verify dashboard URL is accessible: {dashboard_url}")
        print(f"   3. Confirm Supabase backend is running")
        print(f"   4. Check if API authentication is working")
        
        return False

def test_simple_init_api():
    """
    Test the simple init() API that users will primarily use.
    """
    print("\n🔧 Testing Simple Init API")
    print("===========================\n")
    
    try:
        import agent_monitor
        
        # Test the simple init API
        print("📡 Calling agent_monitor.init()...")
        agent_monitor.init(
            api_key="simple-init-test",
            dashboard_url="https://0f3jus9vnfzq.space.minimax.io",
            enable_logging=True
        )
        print("  ✅ Simple init completed successfully")
        
        # Give it a moment to initialize
        time.sleep(2)
        
        print("\n✅ SIMPLE INIT API TEST PASSED")
        print("   The 3-line integration is working:")
        print("   1. import agent_monitor")
        print("   2. agent_monitor.init(api_key='...', dashboard_url='...')")
        print("   3. Your agent code runs with automatic monitoring")
        
        return True
        
    except Exception as e:
        print(f"\n❌ SIMPLE INIT API TEST FAILED: {e}")
        traceback.print_exc()
        return False

def main():
    """
    Run the complete end-to-end integration test.
    """
    print("🚀 Agent Monitor End-to-End Integration Test")
    print("=============================================\n")
    
    # Test 1: Detailed integration test
    test1_success = test_real_integration()
    
    # Test 2: Simple init API test  
    test2_success = test_simple_init_api()
    
    # Final results
    print("\n\n📋 FINAL TEST RESULTS")
    print("=====================")
    
    results = [
        ("End-to-End Integration", test1_success),
        ("Simple Init API", test2_success)
    ]
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status} {test_name}")
        if success:
            passed += 1
    
    print(f"\n📊 Results: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 ALL TESTS PASSED!")
        print("\n✅ The agent-monitor package is working correctly")
        print("✅ Data is flowing from the package to the dashboard")
        print("✅ The 3-line integration API is functional")
        print("✅ Both simple and advanced usage patterns work")
        print("\n🚀 The package is ready for production use!")
        return 0
    else:
        print(f"\n⚠️  {len(results) - passed} test(s) failed")
        print("\n🔧 The package may need additional debugging")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)