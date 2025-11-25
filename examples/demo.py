"""
Curve Intelligence Demo

Demonstrates curve analysis, risk detection, and optimal window calculation.
Perfect for screen recordings and promotional videos.
"""

import sys
import time
from datetime import datetime

# Suppress logging for cleaner output
import logging
logging.getLogger().setLevel(logging.CRITICAL)

def print_header(title: str, char: str = "="):
    """Print formatted header"""
    width = 70
    print("\n" + char * width)
    print(f"  {title}".center(width))
    print(char * width + "\n")

def print_section(title: str):
    """Print section title"""
    print(f"\n{'─' * 70}")
    print(f"  {title}")
    print(f"{'─' * 70}\n")

def print_success(message: str):
    """Print success message"""
    print(f"     ✅ {message}")
    time.sleep(0.2)

def print_info(message: str):
    """Print info message"""
    print(f"     ℹ️  {message}")
    time.sleep(0.2)

def print_data(label: str, value: str):
    """Print data label and value"""
    print(f"     {label:.<30} {value}")

def main():
    """Main demo function"""
    # Clear screen
    print("\n" * 2)
    
    # Header
    print_header("EVALYS CURVE INTELLIGENCE", "═")
    print("  Real-time Curve Analysis, Risk Detection, and Execution Window Optimization")
    print(f"  Demo Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    time.sleep(1)
    
    # Overview
    print_section("OVERVIEW")
    print("  The Curve Intelligence Layer analyzes bonding curves to provide:")
    print("    • Real-time curve metrics (slope, depth, velocity, volatility)")
    print("    • Risk detection (snipers, clusters, liquidity risks)")
    print("    • Pattern recognition (whales, bots, pump/dump)")
    print("    • Optimal execution windows")
    time.sleep(2)
    
    # Simulated Token Analysis
    print_section("TOKEN ANALYSIS")
    
    # Simulated token mint
    token_mint = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
    print_data("Token Mint", token_mint[:32] + "...")
    print_data("Launchpad", "Pump.fun")
    print_data("Analysis Window", "5 minutes")
    time.sleep(1)
    
    # Curve Metrics
    print_section("CURVE METRICS")
    
    try:
        # Simulated curve analysis
        curve_metrics = {
            "slope": 0.65,
            "liquidity_depth": 0.45,
            "trade_velocity": 0.72,
            "volatility": 0.58,
            "price_impact": 0.35,
            "current_price": 0.000123,
            "supply": 1_000_000_000,
            "market_cap": 123_000
        }
        
        print_success("Curve metrics calculated")
        print_data("Slope", f"{curve_metrics['slope']:.2f} (High - rapid growth)")
        print_data("Liquidity Depth", f"{curve_metrics['liquidity_depth']:.2f} (Medium)")
        print_data("Trade Velocity", f"{curve_metrics['trade_velocity']:.2f} (High activity)")
        print_data("Volatility", f"{curve_metrics['volatility']:.2f} (Moderate)")
        print_data("Price Impact", f"{curve_metrics['price_impact']:.2f} (Low)")
        print_data("Current Price", f"{curve_metrics['current_price']:.6f} SOL")
        print_data("Market Cap", f"{curve_metrics['market_cap']:,.0f} SOL")
        time.sleep(1.5)
        
    except Exception as e:
        print(f"     ⚠️  Error: {e}")
        return
    
    # Sniper Detection
    print_section("SNIPER DETECTION")
    
    try:
        from src.curve_intelligence.risk_detector import RiskDetector
        
        detector = RiskDetector()
        
        # Simulated sniper detection
        sniper_result = {
            "is_active": True,
            "sniper_score": 0.75,
            "probability": 0.75,
            "transaction_count": 12,
            "frequency": 0.04,
            "avg_time_between": 8.5,
            "first_seen_ratio": 0.67
        }
        
        print_success("Sniper detection completed")
        print_data("Active", "Yes" if sniper_result["is_active"] else "No")
        print_data("Sniper Score", f"{sniper_result['sniper_score']:.2f}")
        print_data("Probability", f"{sniper_result['probability']:.1%}")
        print_data("Transaction Count", str(sniper_result["transaction_count"]))
        print_data("Frequency", f"{sniper_result['frequency']:.3f} trades/sec")
        print_data("Avg Time Between", f"{sniper_result['avg_time_between']:.1f}s")
        print_data("First-Seen Ratio", f"{sniper_result['first_seen_ratio']:.1%}")
        time.sleep(1.5)
        
    except Exception as e:
        print(f"     ⚠️  Error: {e}")
    
    # Buy Cluster Detection
    print_section("BUY CLUSTER DETECTION")
    
    try:
        # Simulated cluster detection
        clusters = [
            {
                "start_time": int(time.time()) - 180,
                "end_time": int(time.time()) - 120,
                "transaction_count": 5,
                "total_volume": 2.5,
                "correlation_score": 0.68
            },
            {
                "start_time": int(time.time()) - 60,
                "end_time": int(time.time()) - 30,
                "transaction_count": 3,
                "total_volume": 1.8,
                "correlation_score": 0.52
            }
        ]
        
        print_success(f"Detected {len(clusters)} buy clusters")
        for i, cluster in enumerate(clusters, 1):
            print(f"\n     Cluster {i}:")
            print_data("  Transactions", str(cluster["transaction_count"]))
            print_data("  Total Volume", f"{cluster['total_volume']:.2f} SOL")
            print_data("  Correlation", f"{cluster['correlation_score']:.2f}")
        time.sleep(1.5)
        
    except Exception as e:
        print(f"     ⚠️  Error: {e}")
    
    # Risk Assessment
    print_section("RISK ASSESSMENT")
    
    try:
        # Calculate risk score using formula from risk-model.md
        sniper_score = 0.75
        volatility = 0.58
        velocity = 0.72
        liquidity_depth = 0.45
        
        liquidity_risk_inv = 1.0 - liquidity_depth
        velocity_norm = min(1.0, velocity * 1.2)
        
        risk_score = (
            0.35 * sniper_score +
            0.25 * volatility +
            0.20 * velocity_norm +
            0.20 * liquidity_risk_inv
        )
        
        if risk_score >= 0.9:
            risk_level = "critical"
        elif risk_score >= 0.7:
            risk_level = "high"
        elif risk_score >= 0.35:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        print_success("Risk assessment completed")
        print_data("Risk Score", f"{risk_score:.3f}")
        print_data("Risk Level", risk_level.upper())
        print_data("Sniper Component", f"{0.35 * sniper_score:.3f} (35% weight)")
        print_data("Volatility Component", f"{0.25 * volatility:.3f} (25% weight)")
        print_data("Velocity Component", f"{0.20 * velocity_norm:.3f} (20% weight)")
        print_data("Liquidity Component", f"{0.20 * liquidity_risk_inv:.3f} (20% weight)")
        print()
        
        # Privacy mode recommendation
        privacy_modes = {
            "low": "Normal",
            "medium": "Stealth",
            "high": "Max Ghost",
            "critical": "Confidential"
        }
        print_info(f"Recommended Privacy Mode: {privacy_modes[risk_level]}")
        time.sleep(2)
        
    except Exception as e:
        print(f"     ⚠️  Error: {e}")
    
    # Pattern Detection
    print_section("PATTERN DETECTION")
    
    patterns = {
        "sniper_activity": True,
        "buy_clusters": len(clusters),
        "whale_activity": False,
        "bot_patterns": True
    }
    
    print_success("Pattern detection completed")
    print_data("Sniper Activity", "Detected" if patterns["sniper_activity"] else "None")
    print_data("Buy Clusters", str(patterns["buy_clusters"]))
    print_data("Whale Activity", "Detected" if patterns["whale_activity"] else "None")
    print_data("Bot Patterns", "Detected" if patterns["bot_patterns"] else "None")
    time.sleep(1)
    
    # Flags
    flags = ["SNIPER_ACTIVE", "HIGH_SLOPE", "HIGH_VELOCITY", "BOT_PATTERNS"]
    print()
    print("     Detected Flags:")
    for flag in flags:
        print(f"       • {flag}")
    time.sleep(1)
    
    # Optimal Window
    print_section("OPTIMAL EXECUTION WINDOW")
    
    try:
        from src.curve_intelligence.window_optimizer import WindowOptimizer
        
        optimizer = WindowOptimizer()
        
        # Simulated optimal window
        optimal_window = {
            "start_time": int(time.time()) + 30,
            "end_time": int(time.time()) + 90,
            "duration_seconds": 60,
            "confidence": 0.72,
            "reason": "Low volatility period expected"
        }
        
        print_success("Optimal window calculated")
        print_data("Start Time", datetime.fromtimestamp(optimal_window["start_time"]).strftime("%H:%M:%S"))
        print_data("End Time", datetime.fromtimestamp(optimal_window["end_time"]).strftime("%H:%M:%S"))
        print_data("Duration", f"{optimal_window['duration_seconds']} seconds")
        print_data("Confidence", f"{optimal_window['confidence']:.1%}")
        print_data("Reason", optimal_window["reason"])
        time.sleep(1.5)
        
    except Exception as e:
        print(f"     ⚠️  Error: {e}")
    
    # Summary
    print_section("SUMMARY")
    
    print("  Analysis Complete")
    print()
    print("  Key Findings:")
    print(f"    • Risk Level: {risk_level.upper()} (Score: {risk_score:.3f})")
    print(f"    • Sniper Activity: {'Active' if sniper_result['is_active'] else 'None'}")
    print(f"    • Buy Clusters: {len(clusters)} detected")
    print(f"    • Recommended Privacy: {privacy_modes[risk_level]}")
    print()
    print("  Metrics:")
    print(f"    • Curve Slope: {curve_metrics['slope']:.2f}")
    print(f"    • Liquidity Depth: {curve_metrics['liquidity_depth']:.2f}")
    print(f"    • Trade Velocity: {curve_metrics['trade_velocity']:.2f}")
    print(f"    • Volatility: {curve_metrics['volatility']:.2f}")
    print()
    print("  📝 Note: This is a demonstration.")
    print("     Actual analysis requires:")
    print("     • Real Solana RPC connection")
    print("     • On-chain transaction data")
    print("     • Launchpad program account parsing")
    print()
    
    # Footer
    print_header("DEMO COMPLETE", "═")
    print("  Evalys Curve Intelligence - Real-time Analysis for Memecoin Launchpads")
    print("  See docs/curve-spec.md for detailed specifications")
    print("  See docs/detection.md for detection algorithms")
    print("  See docs/risk-model.md for risk calculation")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Demo interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n  Error during demo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

