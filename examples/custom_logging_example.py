"""
Custom Logging Example

This example shows how to use manual logging and tracing
when you want full control over what gets monitored.
"""

import time
import random
from agent_monitor import AgentMonitor

def simulate_data_processing(monitor, data_batch):
    """
    Simulate processing a batch of data with detailed logging.
    """
    batch_id = data_batch["id"]
    items = data_batch["items"]
    
    monitor.trace(f"Starting batch processing", {
        "batch_id": batch_id,
        "item_count": len(items),
        "batch_size": data_batch.get("size", "unknown")
    })
    
    processed_items = []
    errors = []
    
    for i, item in enumerate(items):
        item_id = item.get("id", f"item_{i}")
        
        try:
            monitor.trace(f"Processing item {item_id}", {
                "item_index": i,
                "item_id": item_id,
                "item_type": item.get("type", "unknown")
            })
            
            # Simulate processing time
            processing_time = random.uniform(0.1, 0.5)
            time.sleep(processing_time)
            
            # Simulate occasional errors
            if random.random() < 0.1:  # 10% error rate
                raise ValueError(f"Random processing error for item {item_id}")
            
            # Simulate successful processing
            processed_item = {
                "id": item_id,
                "status": "processed",
                "processing_time": processing_time,
                "result": f"processed_{item_id}"
            }
            processed_items.append(processed_item)
            
            monitor.log("debug", f"Successfully processed item {item_id}", {
                "processing_time": processing_time,
                "result_size": len(str(processed_item))
            })
            
        except Exception as e:
            errors.append({"item_id": item_id, "error": str(e)})
            monitor.error(e, {
                "item_id": item_id,
                "batch_id": batch_id,
                "context": "item_processing"
            })
    
    # Log batch completion
    monitor.log("info", f"Batch {batch_id} processing complete", {
        "batch_id": batch_id,
        "total_items": len(items),
        "processed_items": len(processed_items),
        "error_count": len(errors),
        "success_rate": len(processed_items) / len(items) if items else 0
    })
    
    return {
        "batch_id": batch_id,
        "processed_items": processed_items,
        "errors": errors
    }

def simulate_external_api_call(monitor, api_name, endpoint):
    """
    Simulate an external API call with monitoring.
    """
    monitor.trace(f"Calling external API: {api_name}", {
        "api_name": api_name,
        "endpoint": endpoint,
        "method": "GET"
    })
    
    try:
        # Simulate API call time
        call_duration = random.uniform(0.5, 2.0)
        time.sleep(call_duration)
        
        # Simulate occasional API failures
        if random.random() < 0.05:  # 5% failure rate
            raise ConnectionError(f"Failed to connect to {api_name}")
        
        # Simulate response
        response = {
            "status": "success",
            "data": f"response_from_{api_name}",
            "timestamp": time.time()
        }
        
        monitor.log("info", f"API call to {api_name} successful", {
            "api_name": api_name,
            "duration": call_duration,
            "response_size": len(str(response))
        })
        
        return response
        
    except Exception as e:
        monitor.error(e, {
            "api_name": api_name,
            "endpoint": endpoint,
            "context": "external_api_call"
        })
        raise

def main():
    # Initialize monitoring
    monitor = AgentMonitor(
        dashboard_url="https://0f3jus9vnfzq.space.minimax.io",
        api_key="your-api-key-here",  # Replace with your actual API key
        agent_name="custom_logging_agent",
        group_id="examples",
        metadata={
            "version": "1.2.3",
            "environment": "development",
            "features": ["batch_processing", "api_integration", "error_handling"]
        }
    )
    
    agent_id = monitor.start()
    print(f"Custom logging agent started! Agent ID: {agent_id}")
    
    try:
        # Log startup
        monitor.log("info", "Agent initialization complete", {
            "startup_time": time.time(),
            "configuration": "custom_logging_example"
        })
        
        # Simulate different types of work with custom logging
        
        # 1. Data processing simulation
        print("\n1. Simulating data processing...")
        monitor.update_status("running", {"current_task": "data_processing"})
        
        for batch_num in range(3):
            # Create sample data batch
            data_batch = {
                "id": f"batch_{batch_num + 1}",
                "items": [
                    {"id": f"item_{i}", "type": "data_record"} 
                    for i in range(random.randint(3, 8))
                ],
                "size": "medium"
            }
            
            print(f"Processing batch {batch_num + 1}...")
            result = simulate_data_processing(monitor, data_batch)
            
            print(f"Batch {batch_num + 1}: {len(result['processed_items'])} items processed, "
                  f"{len(result['errors'])} errors")
        
        # 2. External API calls simulation
        print("\n2. Simulating external API calls...")
        monitor.update_status("running", {"current_task": "api_integration"})
        
        apis_to_call = [
            {"name": "weather_service", "endpoint": "/api/v1/weather"},
            {"name": "user_service", "endpoint": "/api/v1/users"},
            {"name": "notification_service", "endpoint": "/api/v1/notify"}
        ]
        
        for api in apis_to_call:
            try:
                print(f"Calling {api['name']}...")
                response = simulate_external_api_call(monitor, api['name'], api['endpoint'])
                print(f"✓ {api['name']} responded successfully")
            except Exception as e:
                print(f"✗ {api['name']} failed: {e}")
        
        # 3. Custom metrics and performance logging
        print("\n3. Logging custom metrics...")
        monitor.update_status("running", {"current_task": "metrics_collection"})
        
        # Log some custom performance metrics
        monitor.log("info", "Performance metrics collected", {
            "memory_usage_mb": random.randint(100, 500),
            "cpu_usage_percent": random.randint(10, 80),
            "cache_hit_rate": random.uniform(0.7, 0.95),
            "active_connections": random.randint(5, 50),
            "queue_length": random.randint(0, 20)
        })
        
        # 4. Structured logging with different levels
        print("\n4. Demonstrating different log levels...")
        
        monitor.log("debug", "Debug information", {"debug_flag": True, "details": "verbose_mode"})
        monitor.log("info", "Informational message", {"process_step": "validation"})
        monitor.log("warning", "Warning about resource usage", {"resource": "memory", "usage": 85})
        
        # Simulate a recoverable error
        try:
            # This will trigger an error log
            raise RuntimeError("Simulated recoverable error")
        except RuntimeError as e:
            monitor.error(e, {"error_type": "recoverable", "recovery_action": "retry_later"})
            print("Logged a simulated error (for demonstration)")
        
        # Final status
        monitor.log("info", "All custom logging demonstrations completed", {
            "total_duration": time.time(),
            "tasks_completed": 4,
            "demonstration_complete": True
        })
        
        monitor.update_status("idle", {"final_state": "demo_complete"})
        
        print("\nCustom logging demonstration complete!")
        print("Check your dashboard to see all the detailed logs and traces.")
        
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
        monitor.log("warning", "Demonstration interrupted", {"reason": "user_interrupt"})
        monitor.update_status("offline", {"shutdown_reason": "interrupted"})
    
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        monitor.error(e, {"context": "main_demo_loop"})
        monitor.update_status("error", {"error_context": "main_execution"})
    
    finally:
        print("Stopping monitoring...")
        monitor.stop()
        print("Custom logging demo finished!")

if __name__ == "__main__":
    main()
