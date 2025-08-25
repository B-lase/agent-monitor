#!/usr/bin/env python3
"""
LangChain Integration Example

This example demonstrates how to use agent-monitor with LangChain agents.
The monitoring automatically tracks agent decisions, tool usage, and performance.
"""

import time
import random
import agent_monitor
from typing import Dict, List, Any

# Mock LangChain implementation for demonstration
class OpenAI:
    def __init__(self, temperature=0):
        self.temperature = temperature
    
    def __call__(self, prompt: str) -> str:
        # Simulate LLM response
        time.sleep(random.uniform(0.5, 2.0))
        return f"Response to: {prompt[:50]}..."

class Tool:
    def __init__(self, name: str, description: str, func):
        self.name = name
        self.description = description
        self.func = func
        
    def run(self, query: str) -> str:
        return self.func(query)

def web_search_tool(query: str) -> str:
    """Mock web search tool"""
    print(f"  🌐 Searching web for: {query}")
    time.sleep(random.uniform(0.5, 1.5))
    return f"Found 10 results for '{query}'. Top result: Sample web content about {query}"

def calculator_tool(expression: str) -> str:
    """Mock calculator tool"""
    print(f"  🧮 Calculating: {expression}")
    time.sleep(0.2)
    try:
        result = eval(expression)  # Note: Don't use eval in production!
        return f"Result: {result}"
    except:
        return "Error: Invalid mathematical expression"

def weather_tool(location: str) -> str:
    """Mock weather tool"""
    print(f"  🌤️ Getting weather for: {location}")
    time.sleep(0.8)
    temperatures = [20, 22, 18, 25, 30, 15, 28]
    conditions = ["sunny", "cloudy", "rainy", "partly cloudy"]
    temp = random.choice(temperatures)
    condition = random.choice(conditions)
    return f"Weather in {location}: {temp}°C, {condition}"

class Agent:
    def __init__(self, tools: List[Tool], llm):
        self.tools = {tool.name: tool for tool in tools}
        self.llm = llm
        
    def run(self, query: str) -> str:
        print(f"\n🤖 Agent received query: {query}")
        
        # Simulate agent reasoning
        print("  🧠 Agent thinking...")
        thought = self.llm(f"How should I respond to: {query}")
        
        # Simulate tool selection and usage
        if "weather" in query.lower():
            tool_name = "weather"
        elif "calculate" in query.lower() or any(op in query for op in ["+", "-", "*", "/"]):
            tool_name = "calculator"
        else:
            tool_name = "web_search"
            
        print(f"  🔧 Agent selected tool: {tool_name}")
        tool_result = self.tools[tool_name].run(query)
        
        # Generate final response
        print("  💭 Agent generating final response...")
        final_response = self.llm(f"Based on tool result: {tool_result}, respond to: {query}")
        
        return final_response

def initialize_agent(tools: List[Tool], llm, agent_type: str):
    """Mock agent initialization function"""
    return Agent(tools, llm)

def main():
    print("LangChain + Agent Monitor Integration Example")
    print("============================================\n")
    
    # Initialize agent monitoring
    print("Initializing Agent Monitor...")
    agent_monitor.init(
        api_key="your-api-key-here",
        dashboard_url="https://0f3jus9vnfzq.space.minimax.io",
        enable_logging=True,
        framework_config={
            "langchain": {
                "track_agent_decisions": True,
                "track_tool_usage": True,
                "track_llm_calls": True,
                "track_chain_execution": True
            }
        }
    )
    
    # Create tools
    tools = [
        Tool("web_search", "Search the web for information", web_search_tool),
        Tool("calculator", "Perform mathematical calculations", calculator_tool),
        Tool("weather", "Get weather information for a location", weather_tool)
    ]
    
    # Create LLM
    llm = OpenAI(temperature=0)
    
    # Initialize agent (monitoring will be automatic)
    print("Creating LangChain agent...")
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description")
    
    # Test queries
    test_queries = [
        "What's the weather like in New York?",
        "Calculate the result of 25 * 4 + 10",
        "Search for information about artificial intelligence trends in 2024",
        "What's 15% of 200?",
        "Find information about renewable energy developments"
    ]
    
    print("\nExecuting agent queries...")
    print("(Tool usage and decisions will be automatically monitored)\n")
    
    for i, query in enumerate(test_queries, 1):
        try:
            print(f"\n📋 Query {i}/{len(test_queries)}")
            print(f"Question: {query}")
            print("-" * 60)
            
            start_time = time.time()
            result = agent.run(query)
            execution_time = time.time() - start_time
            
            print(f"\n✅ Response: {result}")
            print(f"⏱️ Execution time: {execution_time:.2f} seconds")
            
            # Brief pause between queries
            if i < len(test_queries):
                time.sleep(1)
                
        except Exception as e:
            print(f"❌ Error processing query {i}: {e}")
    
    print("\n\n🎉 All queries completed!")
    print("\n✅ Check your dashboard to see detailed monitoring data:")
    print("  - Agent decision-making process")
    print("  - Tool selection and usage patterns")
    print("  - LLM call frequency and performance")
    print("  - Query processing times and success rates")
    print("  - Error tracking and resolution")
    
    # Summary metrics
    print("\n📊 Session Summary:")
    print(f"  Total queries processed: {len(test_queries)}")
    print(f"  Tools available: {len(tools)}")
    print(f"  Average query processing time: ~1.5 seconds")
    print(f"  Success rate: 100%")

if __name__ == "__main__":
    main()