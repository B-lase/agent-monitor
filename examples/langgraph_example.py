#!/usr/bin/env python3
"""
LangGraph Integration Example

This example demonstrates how to use agent-monitor with LangGraph workflows.
The monitoring is automatically integrated when you initialize the monitor.
"""

import time
import agent_monitor
from typing import Dict, Any

# Note: This is a mock LangGraph implementation for demonstration
# In a real scenario, you would import from the actual langgraph package
class StateGraph:
    def __init__(self, state_schema):
        self.state_schema = state_schema
        self.nodes = {}
        self.edges = []
        
    def add_node(self, name: str, func):
        self.nodes[name] = func
        
    def add_edge(self, from_node: str, to_node: str):
        self.edges.append((from_node, to_node))
        
    def compile(self):
        return CompiledGraph(self.nodes, self.edges)

class CompiledGraph:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        
    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # Simulate graph execution
        state = input_data.copy()
        
        # Execute nodes in order (simplified)
        for node_name, node_func in self.nodes.items():
            print(f"Executing node: {node_name}")
            state = node_func(state)
            time.sleep(0.5)  # Simulate processing time
            
        return state

# State schema for our workflow
class WorkflowState:
    def __init__(self):
        self.messages = []
        self.current_step = 0
        self.results = {}

def research_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Research node that gathers information"""
    print("  📚 Gathering research data...")
    state['research_results'] = {
        'sources_found': 5,
        'key_insights': ['Market trending up', 'Increased volatility', 'Strong fundamentals'],
        'confidence': 0.85
    }
    return state

def analysis_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Analysis node that processes the research"""
    print("  🔍 Analyzing research data...")
    research = state.get('research_results', {})
    state['analysis_results'] = {
        'recommendation': 'BUY',
        'risk_level': 'Medium',
        'confidence_score': research.get('confidence', 0.5) * 0.9,
        'target_price': 150.00
    }
    return state

def decision_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Decision node that makes the final recommendation"""
    print("  🎯 Making final decision...")
    analysis = state.get('analysis_results', {})
    state['final_decision'] = {
        'action': analysis.get('recommendation', 'HOLD'),
        'quantity': 100,
        'rationale': 'Based on strong fundamentals and positive market trends',
        'expected_return': 0.15
    }
    return state

def main():
    print("LangGraph + Agent Monitor Integration Example")
    print("=============================================\n")
    
    # Initialize agent monitoring
    print("Initializing Agent Monitor...")
    agent_monitor.init(
        api_key="your-api-key-here",
        dashboard_url="https://0f3jus9vnfzq.space.minimax.io",
        enable_logging=True,
        framework_config={
            "langgraph": {
                "track_state_changes": True,
                "track_node_execution": True,
                "track_edge_traversal": True
            }
        }
    )
    
    # Create the LangGraph workflow
    print("Creating LangGraph workflow...")
    workflow = StateGraph(WorkflowState)
    
    # Add nodes to the workflow
    workflow.add_node("research", research_node)
    workflow.add_node("analysis", analysis_node)
    workflow.add_node("decision", decision_node)
    
    # Add edges to define the flow
    workflow.add_edge("research", "analysis")
    workflow.add_edge("analysis", "decision")
    
    # Compile the workflow
    app = workflow.compile()
    
    print("Executing LangGraph workflow...")
    print("(Monitoring will be automatically handled)\n")
    
    # Execute the workflow - monitoring is automatic
    try:
        result = app.invoke({
            "query": "Should I invest in AAPL stock?",
            "user_id": "investor_123",
            "timestamp": time.time()
        })
        
        print("\n🎉 Workflow completed successfully!")
        print("\nFinal Results:")
        print(f"  Research: {result.get('research_results', {}).get('key_insights', [])}")
        print(f"  Analysis: {result.get('analysis_results', {}).get('recommendation', 'N/A')}")
        print(f"  Decision: {result.get('final_decision', {}).get('action', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Workflow execution failed: {e}")
    
    print("\n✅ Check your dashboard to see the detailed execution trace!")
    print("The monitoring captured:")
    print("  - Node execution times and results")
    print("  - State changes between nodes")
    print("  - Edge traversals and decision points")
    print("  - Overall workflow performance metrics")

if __name__ == "__main__":
    main()