#!/usr/bin/env python3
"""
Performance Monitoring Example

This example demonstrates how to use agent-monitor for detailed performance
tracking and optimization of AI agent operations.
"""

import time
import random
import psutil
import threading
from typing import Dict, List, Any
import agent_monitor
from agent_monitor import AgentMonitor

class PerformanceTracker:
    """Helper class to track system performance metrics"""
    
    def __init__(self, monitor: AgentMonitor):
        self.monitor = monitor
        self.tracking = False
        self.tracking_thread = None
        
    def start_tracking(self, interval: float = 1.0):
        """Start background performance tracking"""
        self.tracking = True
        self.tracking_thread = threading.Thread(
            target=self._track_performance, 
            args=(interval,),
            daemon=True
        )
        self.tracking_thread.start()
        
    def stop_tracking(self):
        """Stop background performance tracking"""
        self.tracking = False
        if self.tracking_thread:
            self.tracking_thread.join()
            
    def _track_performance(self, interval: float):
        """Background thread function to track performance metrics"""
        while self.tracking:
            try:
                # CPU usage
                cpu_percent = psutil.cpu_percent(interval=0.1)
                self.monitor.log_metric("cpu_usage", cpu_percent, "percentage")
                
                # Memory usage
                memory = psutil.virtual_memory()
                self.monitor.log_metric("memory_usage", memory.percent, "percentage")
                self.monitor.log_metric("memory_available", memory.available / (1024**3), "GB")
                
                # Disk I/O (if available)
                try:
                    disk_io = psutil.disk_io_counters()
                    if disk_io:
                        self.monitor.log_metric("disk_read_mb", disk_io.read_bytes / (1024**2), "MB")
                        self.monitor.log_metric("disk_write_mb", disk_io.write_bytes / (1024**2), "MB")
                except:
                    pass  # Disk I/O might not be available in some environments
                    
                time.sleep(interval)
                
            except Exception as e:
                print(f"Performance tracking error: {e}")
                break

class PerformanceOptimizedAgent:
    """An agent designed to demonstrate performance monitoring capabilities"""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.cache = {}
        self.operation_count = 0
        
        # Initialize monitoring
        self.monitor = AgentMonitor(
            agent_id=agent_id,
            agent_name=f"Performance Agent {agent_id}",
            agent_type="performance_optimized",
            metadata={
                "optimization_level": "high",
                "caching_enabled": True,
                "monitoring_interval": 1.0
            }
        )
        
        # Initialize performance tracker
        self.perf_tracker = PerformanceTracker(self.monitor)
        
    def start_monitoring_session(self):
        """Start a comprehensive monitoring session"""
        print(f"📈 Starting performance monitoring for agent {self.agent_id}")
        
        self.monitor.start_session()
        self.perf_tracker.start_tracking(interval=2.0)  # Track every 2 seconds
        
        # Log session initialization
        self.monitor.log_event("performance_session_start", {
            "cache_size": len(self.cache),
            "operation_count": self.operation_count,
            "monitoring_features": ["cpu", "memory", "disk_io", "custom_metrics"]
        })
        
    def simulate_cpu_intensive_task(self, task_name: str, duration: float = 2.0):
        """Simulate a CPU-intensive operation"""
        print(f"  🔧 Executing CPU-intensive task: {task_name}")
        
        start_time = time.time()
        start_cpu = psutil.cpu_percent()
        
        self.monitor.log_event("cpu_task_start", {
            "task_name": task_name,
            "estimated_duration": duration,
            "initial_cpu_usage": start_cpu
        })
        
        # Simulate CPU-intensive work
        end_time = start_time + duration
        calculations = 0
        
        while time.time() < end_time:
            # Perform some calculations
            for i in range(1000):
                _ = sum(range(100))
                calculations += 1
            time.sleep(0.01)  # Small pause to prevent excessive CPU usage
            
        execution_time = time.time() - start_time
        final_cpu = psutil.cpu_percent()
        
        self.monitor.log_event("cpu_task_completion", {
            "task_name": task_name,
            "actual_duration": execution_time,
            "calculations_performed": calculations,
            "final_cpu_usage": final_cpu,
            "cpu_delta": final_cpu - start_cpu
        })
        
        # Log performance metrics
        self.monitor.log_metric("task_duration", execution_time, "seconds")
        self.monitor.log_metric("calculations_per_second", calculations / execution_time, "ops/sec")
        self.monitor.log_metric("cpu_efficiency", calculations / (final_cpu + 1), "ops/cpu_percent")
        
        return {
            "duration": execution_time,
            "calculations": calculations,
            "efficiency": calculations / execution_time
        }
        
    def simulate_memory_intensive_task(self, task_name: str, data_size_mb: int = 50):
        """Simulate a memory-intensive operation"""
        print(f"  💾 Executing memory-intensive task: {task_name} ({data_size_mb}MB)")
        
        start_time = time.time()
        start_memory = psutil.virtual_memory().percent
        
        self.monitor.log_event("memory_task_start", {
            "task_name": task_name,
            "target_data_size_mb": data_size_mb,
            "initial_memory_usage": start_memory
        })
        
        try:
            # Allocate memory
            data_size_bytes = data_size_mb * 1024 * 1024
            large_data = bytearray(data_size_bytes)
            
            # Perform operations on the data
            for i in range(0, len(large_data), 1024):
                large_data[i:i+1024] = bytes(range(256)) * 4
                if i % (data_size_bytes // 10) == 0:  # Check progress
                    current_memory = psutil.virtual_memory().percent
                    progress = (i / data_size_bytes) * 100
                    self.monitor.log_metric("memory_task_progress", progress, "percentage")
            
            # Simulate some processing
            time.sleep(0.5)
            
            # Clean up
            del large_data
            
            execution_time = time.time() - start_time
            final_memory = psutil.virtual_memory().percent
            
            self.monitor.log_event("memory_task_completion", {
                "task_name": task_name,
                "actual_duration": execution_time,
                "data_processed_mb": data_size_mb,
                "final_memory_usage": final_memory,
                "memory_delta": final_memory - start_memory,
                "status": "success"
            })
            
            # Log performance metrics
            self.monitor.log_metric("memory_throughput", data_size_mb / execution_time, "MB/sec")
            self.monitor.log_metric("memory_efficiency", data_size_mb / (final_memory - start_memory + 1), "MB/percent")
            
            return {
                "duration": execution_time,
                "throughput": data_size_mb / execution_time,
                "status": "success"
            }
            
        except MemoryError as e:
            self.monitor.log_event("memory_task_error", {
                "task_name": task_name,
                "error_type": "MemoryError",
                "error_message": str(e),
                "requested_size_mb": data_size_mb
            })
            return {"status": "failed", "error": str(e)}
            
    def simulate_io_intensive_task(self, task_name: str, file_count: int = 10):
        """Simulate an I/O-intensive operation"""
        print(f"  📁 Executing I/O-intensive task: {task_name} ({file_count} files)")
        
        start_time = time.time()
        
        self.monitor.log_event("io_task_start", {
            "task_name": task_name,
            "file_count": file_count,
            "estimated_data_size": f"{file_count * 10}KB"
        })
        
        files_processed = 0
        total_bytes = 0
        
        try:
            for i in range(file_count):
                filename = f"temp_perf_test_{i}.txt"
                data = f"Performance test data for file {i}\n" * 100  # ~3KB per file
                
                # Write file
                with open(filename, 'w') as f:
                    f.write(data)
                    
                # Read file back
                with open(filename, 'r') as f:
                    read_data = f.read()
                    
                total_bytes += len(data.encode())
                files_processed += 1
                
                # Clean up
                import os
                os.remove(filename)
                
                # Log progress
                if i % max(1, file_count // 5) == 0:
                    progress = (i / file_count) * 100
                    self.monitor.log_metric("io_task_progress", progress, "percentage")
                    
                time.sleep(0.05)  # Small delay to simulate real I/O patterns
                
            execution_time = time.time() - start_time
            
            self.monitor.log_event("io_task_completion", {
                "task_name": task_name,
                "actual_duration": execution_time,
                "files_processed": files_processed,
                "total_bytes": total_bytes,
                "status": "success"
            })
            
            # Log performance metrics
            self.monitor.log_metric("io_throughput", total_bytes / execution_time, "bytes/sec")
            self.monitor.log_metric("files_per_second", files_processed / execution_time, "files/sec")
            
            return {
                "duration": execution_time,
                "files_processed": files_processed,
                "throughput": total_bytes / execution_time,
                "status": "success"
            }
            
        except Exception as e:
            self.monitor.log_event("io_task_error", {
                "task_name": task_name,
                "error_type": type(e).__name__,
                "error_message": str(e),
                "files_processed": files_processed
            })
            return {"status": "failed", "error": str(e)}
            
    def run_performance_benchmarks(self):
        """Run a comprehensive set of performance benchmarks"""
        print("\n🏁 Starting Performance Benchmarks")
        print("=====================================\n")
        
        benchmarks = [
            {"type": "cpu", "name": "Matrix Multiplication", "duration": 3.0},
            {"type": "cpu", "name": "Prime Number Generation", "duration": 2.5},
            {"type": "memory", "name": "Large Array Processing", "size_mb": 30},
            {"type": "memory", "name": "Data Transformation", "size_mb": 25},
            {"type": "io", "name": "File Operations", "file_count": 15},
            {"type": "io", "name": "Batch Processing", "file_count": 20}
        ]
        
        results = []
        
        for i, benchmark in enumerate(benchmarks, 1):
            print(f"\n--- Benchmark {i}/{len(benchmarks)}: {benchmark['name']} ---")
            
            try:
                if benchmark['type'] == 'cpu':
                    result = self.simulate_cpu_intensive_task(
                        benchmark['name'], 
                        benchmark['duration']
                    )
                elif benchmark['type'] == 'memory':
                    result = self.simulate_memory_intensive_task(
                        benchmark['name'], 
                        benchmark['size_mb']
                    )
                elif benchmark['type'] == 'io':
                    result = self.simulate_io_intensive_task(
                        benchmark['name'], 
                        benchmark['file_count']
                    )
                    
                result['benchmark'] = benchmark['name']
                result['type'] = benchmark['type']
                results.append(result)
                
                print(f"  ✅ Completed: {result.get('status', 'success')}")
                
                # Brief pause between benchmarks
                time.sleep(1)
                
            except Exception as e:
                print(f"  ❌ Failed: {e}")
                results.append({
                    "benchmark": benchmark['name'],
                    "type": benchmark['type'],
                    "status": "failed",
                    "error": str(e)
                })
                
        return results
        
    def analyze_performance_results(self, results: List[Dict[str, Any]]):
        """Analyze and report on performance results"""
        print("\n📈 Performance Analysis")
        print("========================\n")
        
        successful_benchmarks = [r for r in results if r.get('status') == 'success']
        failed_benchmarks = [r for r in results if r.get('status') == 'failed']
        
        analysis = {
            "total_benchmarks": len(results),
            "successful_benchmarks": len(successful_benchmarks),
            "failed_benchmarks": len(failed_benchmarks),
            "success_rate": len(successful_benchmarks) / len(results) if results else 0,
            "performance_summary": {
                "cpu_benchmarks": [r for r in successful_benchmarks if r['type'] == 'cpu'],
                "memory_benchmarks": [r for r in successful_benchmarks if r['type'] == 'memory'],
                "io_benchmarks": [r for r in successful_benchmarks if r['type'] == 'io']
            }
        }
        
        # Log comprehensive analysis
        self.monitor.log_event("performance_analysis", analysis)
        
        # Calculate and log aggregate metrics
        if successful_benchmarks:
            avg_cpu_efficiency = sum(r.get('efficiency', 0) for r in analysis['performance_summary']['cpu_benchmarks']) / max(1, len(analysis['performance_summary']['cpu_benchmarks']))
            avg_memory_throughput = sum(r.get('throughput', 0) for r in analysis['performance_summary']['memory_benchmarks']) / max(1, len(analysis['performance_summary']['memory_benchmarks']))
            avg_io_throughput = sum(r.get('throughput', 0) for r in analysis['performance_summary']['io_benchmarks']) / max(1, len(analysis['performance_summary']['io_benchmarks']))
            
            self.monitor.log_metric("avg_cpu_efficiency", avg_cpu_efficiency, "ops/sec")
            self.monitor.log_metric("avg_memory_throughput", avg_memory_throughput, "MB/sec")
            self.monitor.log_metric("avg_io_throughput", avg_io_throughput, "bytes/sec")
            self.monitor.log_metric("benchmark_success_rate", analysis['success_rate'], "percentage")
        
        # Print summary
        print(f"Total Benchmarks: {analysis['total_benchmarks']}")
        print(f"Successful: {analysis['successful_benchmarks']}")
        print(f"Failed: {analysis['failed_benchmarks']}")
        print(f"Success Rate: {analysis['success_rate']:.1%}")
        
        if failed_benchmarks:
            print("\n⚠️ Failed Benchmarks:")
            for benchmark in failed_benchmarks:
                print(f"  - {benchmark['benchmark']}: {benchmark.get('error', 'Unknown error')}")
                
        return analysis
        
    def end_monitoring_session(self):
        """End the performance monitoring session"""
        print("\n🏁 Performance monitoring session completed")
        
        # Stop performance tracking
        self.perf_tracker.stop_tracking()
        
        # Log session end
        self.monitor.log_event("performance_session_end", {
            "total_operations": self.operation_count,
            "cache_utilization": len(self.cache),
            "session_summary": "Performance benchmarks completed successfully"
        })
        
        self.monitor.update_status("completed")
        self.monitor.end_session()
        
        print("✅ Check your dashboard for detailed performance analytics!")

def main():
    print("Performance Monitoring Example")
    print("==============================\n")
    
    # Initialize agent monitoring
    print("Initializing Agent Monitor...")
    agent_monitor.init(
        api_key="your-api-key-here",
        dashboard_url="https://0f3jus9vnfzq.space.minimax.io",
        enable_logging=True
    )
    
    # Create performance-optimized agent
    agent = PerformanceOptimizedAgent("perf-agent-001")
    
    try:
        # Start monitoring session
        agent.start_monitoring_session()
        
        # Run performance benchmarks
        results = agent.run_performance_benchmarks()
        
        # Analyze results
        analysis = agent.analyze_performance_results(results)
        
        print("\n🎉 All performance tests completed successfully!")
        
    except KeyboardInterrupt:
        print("\n⏹️ Performance testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error during performance testing: {e}")
        agent.monitor.log_event("fatal_error", {
            "error_type": type(e).__name__,
            "error_message": str(e)
        })
        agent.monitor.update_status("error")
    finally:
        # Always end the session
        agent.end_monitoring_session()

if __name__ == "__main__":
    main()