# Curve Intelligence Specification

## Overview

The Curve Intelligence Layer analyzes bonding curves on Solana launchpads (Pump.fun, Bonk.fun) to provide real-time insights, risk assessment, and optimal execution windows.

## Data Sources

### Primary Sources

1. **Solana RPC**
   - `getSignaturesForAddress`: Fetch transaction signatures for token mint
   - `getTransaction`: Get full transaction details
   - `getAccountInfo`: Fetch bonding curve account state
   - `getTokenAccountBalance`: Get token supply and balances

2. **Launchpad Program Accounts**
   - **Pump.fun**: Bonding curve PDA, associated token accounts
   - **Bonk.fun**: Bonding curve state accounts
   - Fetched via `getAccountInfo` with program-specific parsing

3. **Optional Indexers**
   - Helius, QuickNode, or custom indexer for historical data
   - Used for extended time windows and pattern analysis

### Data Collection Flow

```
1. Fetch recent signatures (last N minutes)
   ↓
2. Get transaction details for each signature
   ↓
3. Parse transaction instructions (buy/sell)
   ↓
4. Extract: wallet, amount, timestamp, price impact
   ↓
5. Fetch current curve state (price, supply, liquidity)
   ↓
6. Aggregate into analysis data structure
```

## Core Metrics

### 1. Curve Slope

**Definition**: Rate of price change per unit of supply

**Calculation**:
```
slope = (price_current - price_previous) / (supply_current - supply_previous)
```

**Normalization**: Slope normalized to [0, 1] based on historical range

**Interpretation**:
- High slope (>0.7): Rapid price increase, low liquidity depth
- Medium slope (0.3-0.7): Steady growth
- Low slope (<0.3): Slow growth or stagnation

### 2. Liquidity Depth

**Definition**: Estimated liquidity available at current price level

**Calculation**:
```
depth = (liquidity_pool / price) * depth_factor
```

Where `depth_factor` accounts for bonding curve mechanics.

**Normalization**: Depth normalized to [0, 1] based on market cap

**Interpretation**:
- High depth (>0.5): Good liquidity, lower slippage risk
- Medium depth (0.2-0.5): Moderate liquidity
- Low depth (<0.2): Thin liquidity, high slippage risk

### 3. Trade Velocity

**Definition**: Rate of transactions per unit time

**Calculation**:
```
velocity = transaction_count / time_window_seconds
```

**Normalization**: Velocity normalized to [0, 1] based on historical max

**Interpretation**:
- High velocity (>0.7): Active trading, potential volatility
- Medium velocity (0.3-0.7): Normal activity
- Low velocity (<0.3): Low activity, potential stagnation

### 4. Volatility Window

**Definition**: Price volatility over a rolling time window

**Calculation**:
```
volatility = std_dev(price_changes) / mean(price)
```

**Normalization**: Volatility normalized to [0, 1]

**Interpretation**:
- High volatility (>0.6): Unstable price, high risk
- Medium volatility (0.3-0.6): Normal price movement
- Low volatility (<0.3): Stable price, lower risk

### 5. Price Impact

**Definition**: Expected price change for a given trade size

**Calculation**:
```
impact = (trade_size / liquidity_depth) * impact_factor
```

**Normalization**: Impact normalized to [0, 1]

**Interpretation**:
- High impact (>0.5): Large trades will move price significantly
- Medium impact (0.2-0.5): Moderate price movement
- Low impact (<0.2): Minimal price movement

## Output Schema

### Analysis Result

```python
{
    "token_mint": str,                    # Token mint address
    "timestamp": str,                     # ISO timestamp
    "curve_metrics": {
        "slope": float,                   # [0, 1] normalized slope
        "liquidity_depth": float,         # [0, 1] normalized depth
        "trade_velocity": float,          # [0, 1] normalized velocity
        "volatility": float,              # [0, 1] normalized volatility
        "price_impact": float,            # [0, 1] normalized impact
        "current_price": float,            # Current price in SOL
        "supply": float,                  # Current token supply
        "market_cap": float               # Estimated market cap
    },
    "risk_score": float,                 # [0, 1] overall risk score
    "risk_level": str,                    # "low" | "medium" | "high" | "critical"
    "flags": List[str],                   # Detected flags (see below)
    "patterns": {                         # Pattern detection results
        "sniper_activity": bool,
        "buy_clusters": int,              # Number of clusters detected
        "whale_activity": bool,
        "bot_patterns": bool
    }
}
```

### Flags

Possible flags in `flags` array:

- `"HIGH_SLOPE"`: Rapid price increase detected
- `"LOW_LIQUIDITY"`: Thin liquidity depth
- `"HIGH_VOLATILITY"`: Unstable price movement
- `"SNIPER_ACTIVE"`: Sniper activity detected
- `"CLUSTER_DETECTED"`: Buy clusters detected
- `"WHALE_ACTIVITY"`: Large wallet activity
- `"BOT_PATTERNS"`: Automated trading patterns
- `"PUMP_SIGNAL"`: Potential pump pattern
- `"DUMP_RISK"`: Potential dump risk

## Data Freshness

- **Real-time**: Analysis uses data from last 5 minutes
- **Recent**: Extended analysis uses data from last 30 minutes
- **Historical**: Pattern recognition uses data from last 24 hours (if available)

## Caching

- Analysis results cached for 30 seconds to reduce RPC load
- Cache key: `token_mint + time_window`
- Cache invalidation on new transactions detected

## Error Handling

- **RPC Failures**: Retry with exponential backoff (max 3 retries)
- **Missing Data**: Return partial analysis with available metrics
- **Invalid Token**: Return error with clear message
- **Rate Limiting**: Respect RPC rate limits, queue requests

## Performance Targets

- **Analysis Latency**: < 2 seconds for real-time analysis
- **API Response Time**: < 500ms for cached results
- **Data Collection**: < 5 seconds for full transaction history fetch

## Future Enhancements

- Machine learning models for pattern recognition
- Multi-chain support (if launchpads expand)
- Real-time WebSocket updates
- Historical backtesting capabilities

