"""
Example usage of Evalys Curve Intelligence
"""

import asyncio
from solders.pubkey import Pubkey
from src.curve_intelligence.intelligence_layer import CurveIntelligenceLayer


async def main():
    """Example usage"""
    print("=" * 60)
    print("Evalys Curve Intelligence - Example")
    print("=" * 60)
    
    # Initialize intelligence layer
    intelligence = CurveIntelligenceLayer(rpc_url="https://api.devnet.solana.com")
    
    try:
        # Example token mint (placeholder)
        token_mint = Pubkey.from_string("11111111111111111111111111111111")
        
        # Example 1: Comprehensive analysis
        print("\n📋 Example 1: Comprehensive Token Analysis")
        try:
            analysis = await intelligence.analyze_token(token_mint)
            print(f"   Token: {analysis['token_mint']}")
            print(f"   Risk Level: {analysis['risk_assessment']['overall_risk']}")
            print(f"   Patterns Detected: {len(analysis['patterns'])}")
        except Exception as e:
            print(f"   Note: {e} (expected for placeholder token)")
        
        # Example 2: Risk assessment
        print("\n📋 Example 2: Risk Assessment")
        try:
            risk = await intelligence.assess_risk(token_mint)
            print(f"   Overall Risk: {risk['overall_risk']}")
            print(f"   Sniper Activity: {risk['sniper_activity']['is_active']}")
            print(f"   Buy Clusters: {len(risk['buy_clusters'])}")
        except Exception as e:
            print(f"   Note: {e} (expected for placeholder token)")
        
        # Example 3: Sniper detection
        print("\n📋 Example 3: Sniper Detection")
        try:
            sniper = await intelligence.detect_sniper_window(token_mint, time_window_minutes=5)
            print(f"   Sniper Active: {sniper['is_active']}")
            print(f"   Risk Level: {sniper['risk_level']}")
            print(f"   Probability: {sniper['probability']:.2f}")
        except Exception as e:
            print(f"   Note: {e} (expected for placeholder token)")
        
        # Example 4: Optimal execution window
        print("\n📋 Example 4: Optimal Execution Window")
        try:
            window = await intelligence.get_optimal_window(
                token_mint,
                intent="buy",
                amount=1.0
            )
            print(f"   Risk Level: {window.risk_level.value}")
            print(f"   Expected Slippage: {window.expected_slippage * 100:.2f}%")
            print(f"   Confidence: {window.confidence:.2f}")
            print(f"   Optimal Time: {window.optimal_time}")
        except Exception as e:
            print(f"   Note: {e} (expected for placeholder token)")
        
        # Example 5: Pattern detection
        print("\n📋 Example 5: Pattern Detection")
        try:
            patterns = await intelligence.detect_patterns(token_mint, time_window_minutes=30)
            print(f"   Patterns Detected: {len(patterns)}")
            for pattern in patterns:
                print(f"   - {pattern['type']} (confidence: {pattern.get('confidence', 0):.2f})")
        except Exception as e:
            print(f"   Note: {e} (expected for placeholder token)")
        
        # Example 6: Trade impact assessment
        print("\n📋 Example 6: Trade Impact Assessment")
        try:
            impact = await intelligence.assess_trade_impact(
                token_mint,
                amount=5.0,
                trade_type="buy"
            )
            print(f"   Trade Type: {impact['trade_type']}")
            print(f"   Estimated Slippage: {impact['estimated_slippage'] * 100:.2f}%")
            print(f"   Price Impact: {impact['estimated_price_impact']:.6f} SOL")
        except Exception as e:
            print(f"   Note: {e} (expected for placeholder token)")
        
    finally:
        await intelligence.close()
    
    print("\n" + "=" * 60)
    print("✅ Examples completed!")
    print("=" * 60)
    print("\n📝 Note: This intelligence layer provides the framework.")
    print("   Actual on-chain data fetching needs to be implemented")
    print("   based on launchpad program structures.")


if __name__ == "__main__":
    asyncio.run(main())

