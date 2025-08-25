#!/usr/bin/env python3
"""
Custom Agent Monitoring Example

This example demonstrates how to use agent-monitor with a custom agent
implementation, showing detailed monitoring of agent internals.
"""

import time
import random
import json
from typing import Dict, List, Any, Optional
import agent_monitor
from agent_monitor import AgentMonitor

class CustomTradingAgent:
    """A custom trading agent that makes investment decisions"""
    
    def __init__(self, agent_id: str, initial_balance: float = 10000.0):
        self.agent_id = agent_id
        self.balance = initial_balance
        self.portfolio = {}
        self.trade_history = []
        self.risk_tolerance = 0.1  # 10% risk tolerance
        
        # Initialize monitoring
        self.monitor = AgentMonitor(
            agent_id=agent_id,
            agent_name=f"Trading Agent {agent_id}",
            agent_type="autonomous",
            metadata={
                "initial_balance": initial_balance,
                "risk_tolerance": self.risk_tolerance,
                "strategy": "momentum_based"
            }
        )
        
    def start_trading_session(self):
        """Start a new trading session"""
        print(f"🚀 Starting trading session for agent {self.agent_id}")
        self.monitor.start_session()
        self.monitor.log_event("session_start", {
            "starting_balance": self.balance,
            "portfolio_size": len(self.portfolio),
            "risk_tolerance": self.risk_tolerance
        })
        
    def analyze_market(self, symbol: str) -> Dict[str, Any]:
        """Analyze market conditions for a given symbol"""
        print(f"  📊 Analyzing market for {symbol}...")
        
        # Simulate market analysis
        time.sleep(random.uniform(0.5, 1.5))
        
        # Generate mock market data
        current_price = random.uniform(50, 500)
        volatility = random.uniform(0.1, 0.8)
        trend = random.choice(['bullish', 'bearish', 'neutral'])
        volume = random.randint(10000, 1000000)
        
        analysis_result = {
            "symbol": symbol,
            "current_price": current_price,
            "volatility": volatility,
            "trend": trend,
            "volume": volume,
            "recommendation": self._get_recommendation(volatility, trend),
            "confidence": random.uniform(0.6, 0.95)
        }
        
        # Log the analysis event
        self.monitor.log_event("market_analysis", analysis_result)
        self.monitor.log_metric("analysis_confidence", analysis_result["confidence"], "percentage")
        self.monitor.log_metric("market_volatility", volatility, "percentage")
        
        return analysis_result
        
    def _get_recommendation(self, volatility: float, trend: str) -> str:
        """Generate buy/sell/hold recommendation based on market conditions"""
        if trend == 'bullish' and volatility < 0.3:
            return 'BUY'
        elif trend == 'bearish' or volatility > 0.6:
            return 'SELL'
        else:
            return 'HOLD'
            
    def execute_trade(self, symbol: str, action: str, quantity: int, price: float) -> bool:
        """Execute a trade based on the decision"""
        print(f"  💰 Executing {action} order: {quantity} shares of {symbol} at ${price:.2f}")
        
        trade_value = quantity * price
        trade_id = len(self.trade_history) + 1
        
        try:
            if action == 'BUY':
                if trade_value > self.balance:
                    raise ValueError("Insufficient balance for purchase")
                    
                self.balance -= trade_value
                self.portfolio[symbol] = self.portfolio.get(symbol, 0) + quantity
                
            elif action == 'SELL':
                if symbol not in self.portfolio or self.portfolio[symbol] < quantity:
                    raise ValueError("Insufficient shares to sell")
                    
                self.balance += trade_value
                self.portfolio[symbol] -= quantity
                if self.portfolio[symbol] == 0:
                    del self.portfolio[symbol]
            
            # Record successful trade
            trade_record = {
                "trade_id": trade_id,
                "symbol": symbol,
                "action": action,
                "quantity": quantity,
                "price": price,
                "value": trade_value,
                "timestamp": time.time(),
                "status": "completed",
                "new_balance": self.balance
            }
            
            self.trade_history.append(trade_record)
            
            # Log successful trade
            self.monitor.log_event("trade_execution", trade_record)
            self.monitor.log_metric("portfolio_value", self._calculate_portfolio_value(), "USD")
            self.monitor.log_metric("cash_balance", self.balance, "USD")
            
            print(f"    ✅ Trade completed successfully (Trade ID: {trade_id})")
            return True
            
        except Exception as e:
            # Log failed trade
            error_record = {
                "trade_id": trade_id,
                "symbol": symbol,
                "action": action,
                "quantity": quantity,
                "price": price,
                "error": str(e),
                "timestamp": time.time(),
                "status": "failed"
            }
            
            self.monitor.log_event("trade_error", error_record)
            print(f"    ❌ Trade failed: {e}")
            return False
            
    def _calculate_portfolio_value(self) -> float:
        """Calculate total portfolio value (simplified)"""
        # In a real scenario, you'd fetch current market prices
        portfolio_value = sum(quantity * random.uniform(50, 500) 
                            for quantity in self.portfolio.values())
        return self.balance + portfolio_value
        
    def make_trading_decision(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Make a trading decision based on market analysis"""
        print(f"\n🎯 Making trading decision for {symbol}")
        
        # Analyze the market
        analysis = self.analyze_market(symbol)
        
        # Log decision-making process
        self.monitor.log_event("decision_process", {
            "symbol": symbol,
            "analysis_input": analysis,
            "risk_tolerance": self.risk_tolerance,
            "current_balance": self.balance,
            "portfolio_exposure": symbol in self.portfolio
        })
        
        recommendation = analysis['recommendation']
        confidence = analysis['confidence']
        price = analysis['current_price']
        
        # Calculate position size based on risk tolerance
        max_position_value = self.balance * self.risk_tolerance
        max_quantity = int(max_position_value / price)
        
        decision = None
        
        if recommendation == 'BUY' and confidence > 0.7 and max_quantity > 0:
            decision = {
                "action": "BUY",
                "symbol": symbol,
                "quantity": max_quantity,
                "price": price,
                "rationale": f"Strong {analysis['trend']} trend with {confidence:.2%} confidence"
            }
        elif recommendation == 'SELL' and symbol in self.portfolio:
            sell_quantity = min(self.portfolio[symbol], max_quantity) if max_quantity > 0 else self.portfolio[symbol]
            decision = {
                "action": "SELL",
                "symbol": symbol,
                "quantity": sell_quantity,
                "price": price,
                "rationale": f"{analysis['trend']} trend detected, reducing risk exposure"
            }
        else:
            decision = {
                "action": "HOLD",
                "symbol": symbol,
                "rationale": "Market conditions do not meet trading criteria"
            }
            
        # Log the final decision
        self.monitor.log_event("trading_decision", decision)
        print(f"  🧠 Decision: {decision['action']} - {decision['rationale']}")
        
        return decision
        
    def run_trading_strategy(self, symbols: List[str], duration_minutes: int = 5):
        """Run the trading strategy for a specified duration"""
        print(f"\n📈 Running trading strategy for {duration_minutes} minutes")
        print(f"Monitoring symbols: {', '.join(symbols)}")
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        cycle_count = 0
        
        while time.time() < end_time:
            cycle_count += 1
            print(f"\n--- Trading Cycle {cycle_count} ---")
            
            self.monitor.log_event("trading_cycle_start", {
                "cycle_number": cycle_count,
                "symbols_to_analyze": symbols,
                "current_balance": self.balance,
                "portfolio_positions": len(self.portfolio)
            })
            
            cycle_start = time.time()
            
            for symbol in symbols:
                try:
                    # Make trading decision
                    decision = self.make_trading_decision(symbol)
                    
                    # Execute trade if decision is to buy or sell
                    if decision['action'] in ['BUY', 'SELL']:
                        success = self.execute_trade(
                            decision['symbol'],
                            decision['action'],
                            decision['quantity'],
                            decision['price']
                        )
                        
                        if success:
                            self.monitor.log_metric("successful_trades", 1, "count")
                        else:
                            self.monitor.log_metric("failed_trades", 1, "count")
                    
                    # Brief pause between symbols
                    time.sleep(0.5)
                    
                except Exception as e:
                    self.monitor.log_event("strategy_error", {
                        "symbol": symbol,
                        "cycle": cycle_count,
                        "error": str(e),
                        "error_type": type(e).__name__
                    })
                    print(f"  ⚠️ Error processing {symbol}: {e}")
            
            cycle_duration = time.time() - cycle_start
            self.monitor.log_metric("cycle_duration", cycle_duration, "seconds")
            
            # Update agent status
            portfolio_value = self._calculate_portfolio_value()
            self.monitor.update_status("running")
            self.monitor.log_metric("total_portfolio_value", portfolio_value, "USD")
            
            print(f"\n💼 End of cycle {cycle_count}:")
            print(f"   Cash Balance: ${self.balance:.2f}")
            print(f"   Portfolio Value: ${portfolio_value:.2f}")
            print(f"   Total Trades: {len(self.trade_history)}")
            
            # Wait before next cycle (simulate real-time trading intervals)
            time.sleep(random.uniform(10, 30) if duration_minutes > 2 else 2)
        
        print(f"\n🏁 Trading strategy completed after {cycle_count} cycles")
        
    def end_trading_session(self):
        """End the current trading session"""
        final_balance = self.balance
        final_portfolio_value = self._calculate_portfolio_value()
        total_trades = len(self.trade_history)
        
        session_summary = {
            "final_balance": final_balance,
            "final_portfolio_value": final_portfolio_value,
            "total_trades": total_trades,
            "profitable_trades": sum(1 for trade in self.trade_history 
                                   if trade.get('status') == 'completed'),
            "session_duration": time.time()
        }
        
        print(f"\n🎯 Trading session summary:")
        print(f"   Final Cash Balance: ${final_balance:.2f}")
        print(f"   Final Portfolio Value: ${final_portfolio_value:.2f}")
        print(f"   Total Trades Executed: {total_trades}")
        print(f"   Active Positions: {len(self.portfolio)}")
        
        self.monitor.log_event("session_end", session_summary)
        self.monitor.update_status("completed")
        self.monitor.end_session()
        
        print("\n✅ Trading session ended. Check dashboard for detailed analytics!")

def main():
    print("Custom Agent Monitoring Example")
    print("===============================\n")
    
    # Initialize agent monitoring system
    print("Initializing Agent Monitor...")
    agent_monitor.init(
        api_key="your-api-key-here",
        dashboard_url="https://0f3jus9vnfzq.space.minimax.io",
        enable_logging=True
    )
    
    # Create custom trading agent
    agent = CustomTradingAgent(
        agent_id="custom-trader-001",
        initial_balance=25000.0
    )
    
    # Symbols to trade
    symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
    
    try:
        # Start trading session
        agent.start_trading_session()
        
        # Run trading strategy
        agent.run_trading_strategy(symbols, duration_minutes=3)
        
    except KeyboardInterrupt:
        print("\n⏹️ Trading interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        agent.monitor.log_event("fatal_error", {
            "error_type": type(e).__name__,
            "error_message": str(e)
        })
        agent.monitor.update_status("error")
    finally:
        # Always end the session
        agent.end_trading_session()

if __name__ == "__main__":
    main()