#!/usr/bin/env python3
"""
Test Agent Monitor Package

A simple test script to verify that the agent-monitor package is working correctly.
Run this script to test basic functionality before using the package in your projects.
"""

import time
import sys
import traceback

def test_basic_import():
    """Test if the package can be imported successfully"""
    print("Testing package import...")
    try:
        import agent_monitor
        from agent_monitor import AgentMonitor
        print("  ✅ Package imported successfully")
        return True
    except ImportError as e:
        print(f"  ❌ Import failed: {e}")
        return False

def test_initialization():
    """Test agent monitor initialization"""
    print("\nTesting initialization...")
    try:
        import agent_monitor
        
        # Test with mock credentials
        agent_monitor.init(
            api_key="test-api-key",
            dashboard_url="https://test-dashboard.example.com",
            enable_logging=True
        )
        print("  ✅ Initialization completed")
        return True
    except Exception as e:
        print(f"  ❌ Initialization failed: {e}")
        return False

def test_agent_monitor_creation():
    """Test creating an AgentMonitor instance"""
    print("\nTesting AgentMonitor creation...")
    try:
        from agent_monitor import AgentMonitor
        
        monitor = AgentMonitor(
            agent_id="test-agent",
            agent_name="Test Agent",
            agent_type="test",
            metadata={"test": True, "version": "1.0.0"}
        )
        print("  ✅ AgentMonitor instance created successfully")
        return True, monitor
    except Exception as e:
        print(f"  ❌ AgentMonitor creation failed: {e}")
        return False, None

def test_session_management(monitor):
    """Test session start and end functionality"""
    print("\nTesting session management...")
    try:
        if not monitor:
            print("  ⏭️ Skipped (no monitor instance)")
            return False
            
        monitor.start_session()
        print("  ✅ Session started")
        
        time.sleep(1)  # Brief pause
        
        monitor.end_session()
        print("  ✅ Session ended")
        return True
    except Exception as e:
        print(f"  ❌ Session management failed: {e}")
        return False

def test_event_logging(monitor):
    """Test event logging functionality"""
    print("\nTesting event logging...")
    try:
        if not monitor:
            print("  ⏭️ Skipped (no monitor instance)")
            return False
            
        monitor.start_session()
        
        # Test various event types
        test_events = [
            ("initialization", {"test": True, "timestamp": time.time()}),
            ("decision", {"action": "test_action", "confidence": 0.95}),
            ("completion", {"status": "success", "duration": 1.23}),
            ("error", {"error_type": "TestError", "message": "This is a test error"})
        ]
        
        for event_type, data in test_events:
            monitor.log_event(event_type, data)
            print(f"    ✅ Logged {event_type} event")
            time.sleep(0.2)
            
        monitor.end_session()
        print("  ✅ All events logged successfully")
        return True
    except Exception as e:
        print(f"  ❌ Event logging failed: {e}")
        return False

def test_metric_logging(monitor):
    """Test metric logging functionality"""
    print("\nTesting metric logging...")
    try:
        if not monitor:
            print("  ⏭️ Skipped (no monitor instance)")
            return False
            
        monitor.start_session()
        
        # Test various metric types
        test_metrics = [
            ("response_time", 1.234, "seconds"),
            ("accuracy", 0.95, "percentage"),
            ("memory_usage", 128.5, "MB"),
            ("requests_per_second", 42.7, "req/sec")
        ]
        
        for metric_name, value, unit in test_metrics:
            monitor.log_metric(metric_name, value, unit)
            print(f"    ✅ Logged {metric_name}: {value} {unit}")
            time.sleep(0.2)
            
        monitor.end_session()
        print("  ✅ All metrics logged successfully")
        return True
    except Exception as e:
        print(f"  ❌ Metric logging failed: {e}")
        return False

def test_status_updates(monitor):
    """Test status update functionality"""
    print("\nTesting status updates...")
    try:
        if not monitor:
            print("  ⏭️ Skipped (no monitor instance)")
            return False
            
        monitor.start_session()
        
        # Test different status updates
        statuses = ["idle", "running", "paused", "running", "completed"]
        
        for status in statuses:
            monitor.update_status(status)
            print(f"    ✅ Status updated to: {status}")
            time.sleep(0.3)
            
        monitor.end_session()
        print("  ✅ All status updates completed")
        return True
    except Exception as e:
        print(f"  ❌ Status updates failed: {e}")
        return False

def test_error_handling():
    """Test error handling and edge cases"""
    print("\nTesting error handling...")
    try:
        from agent_monitor import AgentMonitor
        
        # Test with minimal parameters
        monitor = AgentMonitor(
            agent_id="error-test-agent",
            agent_name="Error Test Agent"
        )
        
        monitor.start_session()
        
        # Test with various edge cases
        monitor.log_event("test", {})  # Empty data
        monitor.log_event("test", {"complex": {"nested": {"data": [1, 2, 3]}}})  # Complex data
        monitor.log_metric("test_metric", 0.0)  # Zero value
        monitor.update_status("custom_status")  # Custom status
        
        monitor.end_session()
        print("  ✅ Error handling tests passed")
        return True
    except Exception as e:
        print(f"  ❌ Error handling test failed: {e}")
        return False

def run_comprehensive_test():
    """Run a comprehensive integration test"""
    print("\nRunning comprehensive integration test...")
    try:
        from agent_monitor import AgentMonitor
        
        monitor = AgentMonitor(
            agent_id="comprehensive-test",
            agent_name="Comprehensive Test Agent",
            agent_type="testing",
            metadata={"test_type": "comprehensive", "duration": 30}
        )
        
        monitor.start_session()
        print("  ✅ Test session started")
        
        # Simulate a realistic agent workflow
        monitor.log_event("initialization", {"model": "test-model", "config": {"temperature": 0.7}})
        monitor.update_status("running")
        
        for i in range(5):
            # Simulate task processing
            monitor.log_event("task_start", {"task_id": i, "task_type": "test_task"})
            monitor.log_metric("task_progress", (i / 5) * 100, "percentage")
            time.sleep(0.5)
            
            monitor.log_event("task_completion", {"task_id": i, "status": "success"})
            monitor.log_metric("tasks_completed", i + 1, "count")
            
        monitor.update_status("completed")
        monitor.log_event("workflow_completion", {"total_tasks": 5, "success_rate": 100})
        
        monitor.end_session()
        print("  ✅ Comprehensive test completed successfully")
        return True
    except Exception as e:
        print(f"  ❌ Comprehensive test failed: {e}")
        print(f"  Error details: {traceback.format_exc()}")
        return False

def main():
    """Run all tests"""
    print("🧪 Agent Monitor Package Test Suite")
    print("=====================================\n")
    
    # List of all tests
    tests = [
        ("Package Import", test_basic_import),
        ("Initialization", test_initialization),
    ]
    
    # Run basic tests first
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
        
        if not result:
            print(f"\n❌ Critical test '{test_name}' failed. Stopping test suite.")
            break
    else:
        # Run tests that require a monitor instance
        success, monitor = test_agent_monitor_creation()
        results.append(("AgentMonitor Creation", success))
        
        if success:
            monitor_tests = [
                ("Session Management", lambda: test_session_management(monitor)),
                ("Event Logging", lambda: test_event_logging(monitor)),
                ("Metric Logging", lambda: test_metric_logging(monitor)),
                ("Status Updates", lambda: test_status_updates(monitor)),
                ("Error Handling", test_error_handling),
                ("Comprehensive Integration", run_comprehensive_test)
            ]
            
            for test_name, test_func in monitor_tests:
                result = test_func()
                results.append((test_name, result))
    
    # Print test summary
    print("\n\n📈 Test Results Summary")
    print("=======================\n")
    
    passed_tests = sum(1 for _, result in results if result)
    total_tests = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} {test_name}")
    
    print(f"\n📊 Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! The agent-monitor package is working correctly.")
        print("\nYou can now use the package in your projects with confidence.")
        print("\nNext steps:")
        print("1. Replace 'test-api-key' and 'test-dashboard-url' with your actual credentials")
        print("2. Check out the examples in the examples/ directory")
        print("3. Integrate the package with your AI agents")
        print("4. Monitor your agents on your dashboard")
    else:
        print(f"⚠️ {total_tests - passed_tests} tests failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Make sure all dependencies are installed: pip install -e .")
        print("2. Check your Python version (3.7+ required)")
        print("3. Verify network connectivity if using real API endpoints")
        
        return 1  # Exit with error code
        
    return 0  # Success

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)