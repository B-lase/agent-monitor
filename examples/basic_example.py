"""
Basic Agent Monitor Example

This example shows the simplest way to get started with agent monitoring.
Just 3 lines of code to start monitoring any Python application!
"""

import time
from agent_monitor import AgentMonitor

def main():
    # Initialize the monitor with your dashboard URL and API key
    monitor = AgentMonitor(
        dashboard_url="https://0f3jus9vnfzq.space.minimax.io",
        api_key="your-api-key-here",  # Replace with your actual API key
        agent_name="basic_example_agent",
        group_id="examples"
    )
    
    # Start monitoring - this automatically detects your environment
    # and begins sending data to the dashboard
    agent_id = monitor.start()
    print(f"Monitoring started! Agent ID: {agent_id}")
    print("Check your dashboard to see the agent appear in real-time!")
    
    try:
        # Simulate some agent work
        for i in range(10):
            print(f"Doing work iteration {i+1}...")
            
            # Log what we're doing
            monitor.log("info", f"Starting work iteration {i+1}")
            
            # Simulate some processing time
            time.sleep(3)
            
            # Log completion
            monitor.log("info", f"Completed work iteration {i+1}")
            
            # Update status occasionally
            if i % 3 == 0:
                monitor.update_status("running", {"iteration": i+1})
        
        # All done
        monitor.log("info", "All work completed successfully!")
        monitor.update_status("idle")
        
    except KeyboardInterrupt:
        print("\nStopping agent...")
        monitor.log("warning", "Agent stopped by user")
    
    except Exception as e:
        print(f"Error occurred: {e}")
        monitor.error(e, {"context": "main_loop"})
        monitor.update_status("error")
    
    finally:
        # Always stop monitoring gracefully
        print("Stopping monitoring...")
        monitor.stop()
        print("Monitoring stopped.")

if __name__ == "__main__":
    main()
