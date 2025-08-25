#!/usr/bin/env python3
"""
Basic Agent Monitor Usage Example

This example demonstrates the fundamental usage of the agent-monitor package
for tracking a simple AI agent's execution.
"""

import time
import random
import agent_monitor
from agent_monitor import AgentMonitor

def main():
    # SECURITY: Use environment variables for API keys
    # Set environment variable: AGENT_MONITOR_API_KEY=your-service-role-key
    import os
    api_key = os.getenv('AGENT_MONITOR_API_KEY')
    if not api_key:
        print("Error: AGENT_MONITOR_API_KEY environment variable is required")
        print("Set it with: export AGENT_MONITOR_API_KEY=your-service-role-key")
        return
    
    # Initialize the monitoring system
    print("Initializing Agent Monitor...")
    agent_monitor.init(
        api_key=api_key,  # Use environment variable for security
        dashboard_url="https://0f3jus9vnfzq.space.minimax.io",  # Dashboard URL
        enable_logging=True
    )
    
    # Create a monitor for our agent
    monitor = AgentMonitor(
        agent_id="basic-example-agent",
        agent_name="Basic Example Agent",
        agent_type="autonomous",
        metadata={
            "version": "1.0.0",
            "environment": "development",
            "creator": "example-user"
        }
    )
    
    print("Starting agent session...")
    monitor.start_session()
    
    try:
        # Simulate agent initialization
        print("Agent initializing...")
        monitor.log_event("initialization", {
            "model": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 2000,
            "tools_loaded": ["calculator", "web_search", "file_reader"]
        })
        monitor.update_status("running")
        time.sleep(1)
        
        # Simulate some agent work
        tasks = [
            {"task": "analyze_data", "duration": 2, "success_rate": 0.9},
            {"task": "generate_report", "duration": 3, "success_rate": 0.95},
            {"task": "send_notification", "duration": 1, "success_rate": 0.99}
        ]
        
        for i, task in enumerate(tasks, 1):
            print(f"Executing task {i}: {task['task']}")
            
            # Log task start
            monitor.log_event("task_start", {
                "task_id": i,
                "task_name": task['task'],
                "estimated_duration": task['duration']
            })
            
            # Simulate task execution
            start_time = time.time()
            time.sleep(task['duration'])
            execution_time = time.time() - start_time
            
            # Simulate success/failure based on success rate
            success = random.random() < task['success_rate']
            
            if success:
                monitor.log_event("task_completion", {
                    "task_id": i,
                    "task_name": task['task'],
                    "status": "success",
                    "execution_time": execution_time,
                    "output_size": random.randint(100, 1000)
                })
                print(f"  ✅ Task {i} completed successfully")
            else:
                monitor.log_event("task_error", {
                    "task_id": i,
                    "task_name": task['task'],
                    "status": "failed",
                    "execution_time": execution_time,
                    "error_message": f"Task {task['task']} failed during execution"
                })
                print(f"  ❌ Task {i} failed")
            
            # Log performance metrics
            monitor.log_metric("task_duration", execution_time, "seconds")
            monitor.log_metric("memory_usage", random.uniform(50, 200), "MB")
            monitor.log_metric("cpu_usage", random.uniform(10, 80), "percentage")
        
        # Agent work completed
        monitor.log_event("workflow_completion", {
            "total_tasks": len(tasks),
            "successful_tasks": sum(1 for task in tasks if random.random() < task['success_rate']),
            "total_execution_time": sum(task['duration'] for task in tasks)
        })
        monitor.update_status("completed")
        print("Agent workflow completed successfully!")
        
    except Exception as e:
        # Handle any errors that occur during execution
        print(f"Error occurred: {e}")
        monitor.log_event("error", {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "context": "main_execution_loop"
        })
        monitor.update_status("error")
    
    finally:
        # Always end the session
        print("Ending agent session...")
        monitor.end_session()
        print("Monitoring session ended. Check your dashboard for results!")

if __name__ == "__main__":
    main()