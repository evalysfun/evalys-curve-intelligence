# Detection Algorithms

## Overview

This document specifies the algorithms used for detecting snipers, buy clusters, and other patterns in bonding curve activity.

## Sniper Detection (v0.1)

### Definition

A **sniper burst** is a pattern of rapid, coordinated transactions that typically indicates automated trading bots attempting to front-run or copy-trade.

### Algorithm

**Inputs**:
- `transactions`: List of transactions in time window
- `time_window_seconds`: Analysis window (default: 300s = 5 minutes)
- `min_trade_count`: Minimum trades to consider (default: 5)
- `max_trade_size_sol`: Maximum trade size to consider (default: 0.5 SOL)
- `first_seen_threshold`: Minimum % of first-seen wallets (default: 0.6)

**Process**:

1. **Filter transactions**:
   ```python
   filtered = [
       tx for tx in transactions
       if tx.amount <= max_trade_size_sol
       and tx.timestamp >= (now - time_window_seconds)
   ]
   ```

2. **Calculate indicators**:
   ```python
   transaction_count = len(filtered)
   time_span = time_window_seconds
   frequency = transaction_count / time_span
   
   # Calculate time intervals
   timestamps = sorted([tx.timestamp for tx in filtered])
   intervals = [timestamps[i+1] - timestamps[i] 
                for i in range(len(timestamps)-1)]
   avg_interval = mean(intervals) if intervals else 0
   
   # First-seen wallet ratio
   wallets = set(tx.wallet for tx in filtered)
   first_seen_count = count_first_seen_wallets(wallets)
   first_seen_ratio = first_seen_count / len(wallets) if wallets else 0
   
   # Price impact per trade
   price_impacts = [tx.price_impact for tx in filtered]
   avg_price_impact = mean(price_impacts) if price_impacts else 0
   ```

3. **Calculate sniper score**:
   ```python
   # Frequency component (0-0.4)
   frequency_score = min(0.4, frequency * 2)
   
   # Interval component (0-0.3)
   interval_score = 0.3 if avg_interval < 10 else 0.0
   
   # First-seen component (0-0.2)
   first_seen_score = 0.2 if first_seen_ratio >= first_seen_threshold else 0.0
   
   # Price impact component (0-0.1)
   impact_score = min(0.1, avg_price_impact * 0.2)
   
   sniper_score = frequency_score + interval_score + first_seen_score + impact_score
   sniper_score = min(1.0, sniper_score)  # Clamp to [0, 1]
   ```

4. **Determine activity**:
   ```python
   is_active = (
       transaction_count >= min_trade_count
       and sniper_score >= 0.6
   )
   ```

**Output**:
```python
{
    "is_active": bool,
    "sniper_score": float,  # [0, 1]
    "probability": float,    # Same as sniper_score
    "transaction_count": int,
    "frequency": float,     # trades/second
    "avg_time_between": float,  # seconds
    "first_seen_ratio": float,
    "avg_price_impact": float,
    "indicators": {
        "frequency_score": float,
        "interval_score": float,
        "first_seen_score": float,
        "impact_score": float
    }
}
```

### Thresholds

- **Active**: `sniper_score >= 0.6` AND `transaction_count >= 5`
- **High Risk**: `sniper_score >= 0.8`
- **Critical**: `sniper_score >= 0.9` AND `frequency > 0.2`

## Buy Cluster Detection (v0.1)

### Definition

A **buy cluster** is a group of transactions from correlated wallets with similar timing and size patterns, indicating coordinated activity.

### Algorithm

**Inputs**:
- `transactions`: List of transactions
- `cluster_window_seconds`: Time window for clustering (default: 60s)
- `min_cluster_size`: Minimum transactions per cluster (default: 2)
- `size_correlation_threshold`: Size similarity threshold (default: 0.3)

**Process**:

1. **Time-based clustering**:
   ```python
   sorted_txs = sorted(transactions, key=lambda t: t.timestamp)
   clusters = []
   current_cluster = []
   cluster_start = None
   
   for tx in sorted_txs:
       if cluster_start is None:
           cluster_start = tx.timestamp
           current_cluster = [tx]
       elif tx.timestamp - cluster_start <= cluster_window_seconds:
           current_cluster.append(tx)
       else:
           # Save cluster if large enough
           if len(current_cluster) >= min_cluster_size:
               clusters.append(current_cluster)
           # Start new cluster
           cluster_start = tx.timestamp
           current_cluster = [tx]
   
   # Save last cluster
   if len(current_cluster) >= min_cluster_size:
       clusters.append(current_cluster)
   ```

2. **Wallet correlation analysis**:
   ```python
   for cluster in clusters:
       wallets = [tx.wallet for tx in cluster]
       unique_wallets = set(wallets)
       
       # Check for wallet correlation
       wallet_correlation = len(unique_wallets) / len(wallets)
       # Low correlation = same wallets repeating (suspicious)
       
       # Check size similarity
       amounts = [tx.amount for tx in cluster]
       size_std = std_dev(amounts)
       size_mean = mean(amounts)
       size_cv = size_std / size_mean if size_mean > 0 else 0
       # Low CV = similar sizes (suspicious)
       
       cluster.correlation_score = (
           (1 - wallet_correlation) * 0.5 +  # Same wallets = higher score
           (1 - min(1.0, size_cv)) * 0.5      # Similar sizes = higher score
       )
   ```

3. **Filter and rank clusters**:
   ```python
   significant_clusters = [
       cluster for cluster in clusters
       if cluster.correlation_score >= size_correlation_threshold
   ]
   
   # Sort by correlation score (highest first)
   significant_clusters.sort(key=lambda c: c.correlation_score, reverse=True)
   ```

**Output**:
```python
[
    {
        "start_time": int,              # Unix timestamp
        "end_time": int,                 # Unix timestamp
        "transaction_count": int,
        "total_volume": float,          # SOL
        "unique_wallets": int,
        "correlation_score": float,      # [0, 1]
        "avg_amount": float,
        "size_std": float
    },
    ...
]
```

### Thresholds

- **Significant Cluster**: `correlation_score >= 0.3` AND `transaction_count >= 2`
- **High Correlation**: `correlation_score >= 0.6`
- **Suspicious**: `correlation_score >= 0.8` AND `unique_wallets / transaction_count < 0.5`

## Whale Activity Detection

### Definition

**Whale activity** is detected when large transactions (> threshold) occur, indicating significant capital movement.

### Algorithm

**Inputs**:
- `transactions`: List of transactions
- `whale_threshold_sol`: Minimum amount for whale (default: 5.0 SOL)
- `time_window_seconds`: Analysis window (default: 300s)

**Process**:

```python
whale_txs = [
    tx for tx in transactions
    if tx.amount >= whale_threshold_sol
    and tx.timestamp >= (now - time_window_seconds)
]

whale_activity = {
    "is_active": len(whale_txs) > 0,
    "whale_count": len(whale_txs),
    "total_volume": sum(tx.amount for tx in whale_txs),
    "largest_trade": max((tx.amount for tx in whale_txs), default=0),
    "wallets": list(set(tx.wallet for tx in whale_txs))
}
```

**Output**:
```python
{
    "is_active": bool,
    "whale_count": int,
    "total_volume": float,
    "largest_trade": float,
    "unique_wallets": int
}
```

## Bot Pattern Detection

### Definition

**Bot patterns** are detected through analysis of transaction timing, size patterns, and wallet behavior that indicate automated trading.

### Algorithm

**Inputs**:
- `transactions`: List of transactions
- `time_window_seconds`: Analysis window (default: 600s)

**Process**:

```python
# Check for regular intervals (bot-like)
intervals = calculate_intervals(transactions)
interval_std = std_dev(intervals)
interval_mean = mean(intervals) if intervals else 0
regularity_score = 1 - (interval_std / interval_mean) if interval_mean > 0 else 0

# Check for consistent sizes
amounts = [tx.amount for tx in transactions]
amount_cv = std_dev(amounts) / mean(amounts) if mean(amounts) > 0 else 0
consistency_score = 1 - min(1.0, amount_cv)

# Check for wallet reuse
wallets = [tx.wallet for tx in transactions]
unique_wallets = set(wallets)
reuse_ratio = len(wallets) / len(unique_wallets) if unique_wallets else 0

bot_score = (
    regularity_score * 0.4 +
    consistency_score * 0.3 +
    min(1.0, reuse_ratio) * 0.3
)
```

**Output**:
```python
{
    "is_detected": bool,        # bot_score >= 0.6
    "bot_score": float,         # [0, 1]
    "regularity_score": float,
    "consistency_score": float,
    "reuse_ratio": float
}
```

## False Positive Handling

### Strategies

1. **Confidence Thresholds**: Require multiple indicators to agree
2. **Time-based Validation**: Require pattern to persist over multiple windows
3. **Context Awareness**: Consider overall market conditions
4. **Manual Override**: Allow manual flagging/unflagging

### Current Approach

- **Sniper Detection**: Requires `sniper_score >= 0.6` AND `transaction_count >= 5`
- **Cluster Detection**: Requires `correlation_score >= 0.3` AND `transaction_count >= 2`
- **Bot Detection**: Requires `bot_score >= 0.6` AND `transaction_count >= 3`

## Future Improvements

- Machine learning models for pattern recognition
- Multi-wallet correlation analysis
- Cross-token pattern detection
- Historical pattern matching
- Real-time adaptive thresholds

