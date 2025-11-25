# Risk Model Specification

## Overview

The risk model calculates an overall risk score for a token based on multiple factors: sniper activity, buy clusters, liquidity depth, volatility, and trade velocity.

## Risk Score Formula (v0.1)

### Inputs

1. **Sniper Score** (`sniper_score`): [0, 1] from sniper detection
2. **Cluster Risk** (`cluster_risk`): [0, 1] based on number and correlation of clusters
3. **Liquidity Risk** (`liquidity_risk`): [0, 1] based on liquidity depth
4. **Volatility** (`volatility`): [0, 1] normalized volatility
5. **Trade Velocity** (`velocity`): [0, 1] normalized trade velocity

### Formula

```python
risk_score = (
    0.35 * sniper_score +
    0.25 * volatility +
    0.20 * velocity_norm +
    0.20 * liquidity_risk_inv
)
```

Where:
- `velocity_norm = min(1.0, velocity * 1.2)` - Velocity normalized with cap
- `liquidity_risk_inv = 1.0 - liquidity_depth` - Inverse of liquidity depth

### Component Calculations

#### Sniper Score
- Direct from sniper detection algorithm
- Range: [0, 1]
- Weight: 35%

#### Volatility
- Normalized volatility from curve analysis
- Range: [0, 1]
- Weight: 25%

#### Trade Velocity
- Normalized trade velocity from curve analysis
- Range: [0, 1] (capped at 1.0)
- Weight: 20%

#### Liquidity Risk (Inverse)
- Calculated as `1.0 - liquidity_depth`
- Low liquidity = high risk
- Range: [0, 1]
- Weight: 20%

#### Cluster Risk (Optional)
- If clusters detected: `cluster_risk = min(1.0, cluster_count * 0.2)`
- Can be added to formula with weight 0.1 (reducing other weights proportionally)

## Risk Levels

### Thresholds

```python
if risk_score >= 0.9:
    risk_level = "critical"
elif risk_score >= 0.7:
    risk_level = "high"
elif risk_score >= 0.35:
    risk_level = "medium"  # Stealth mode recommended
else:
    risk_level = "low"     # Normal mode acceptable
```

### Risk Level Mapping

| Risk Score | Level | Privacy Mode Recommendation | Description |
|------------|-------|----------------------------|-------------|
| [0.0, 0.35) | Low | Normal | Low risk, standard execution acceptable |
| [0.35, 0.7) | Medium | Stealth | Moderate risk, use privacy techniques |
| [0.7, 0.9) | High | Max Ghost | High risk, aggressive privacy needed |
| [0.9, 1.0] | Critical | Confidential | Critical risk, avoid or use confidential compute |

## Risk Score Interpretation

### Low Risk (0.0 - 0.35)

**Characteristics**:
- No sniper activity detected
- Low volatility
- Good liquidity depth
- Normal trade velocity

**Recommendation**: Standard execution acceptable, minimal privacy needed.

### Medium Risk (0.35 - 0.7)

**Characteristics**:
- Some sniper activity or clusters
- Moderate volatility
- Adequate liquidity
- Elevated trade velocity

**Recommendation**: Use privacy techniques (order slicing, timing jitter, relay routing).

### High Risk (0.7 - 0.9)

**Characteristics**:
- Active sniper activity
- High volatility
- Thin liquidity
- Very high trade velocity

**Recommendation**: Aggressive privacy (max ghost mode, multi-hop routing, extensive slicing).

### Critical Risk (0.9 - 1.0)

**Characteristics**:
- Intense sniper activity
- Extreme volatility
- Very thin liquidity
- Abnormal trade patterns

**Recommendation**: Avoid execution or use confidential compute (Arcium gMPC).

## Risk Monotonicity

**Invariant**: Increasing risk score cannot reduce privacy recommendations.

**Enforcement**:
- Risk levels are strictly ordered: Low < Medium < High < Critical
- Privacy mode recommendations are monotonic: Normal < Stealth < Max Ghost < Confidential
- Higher risk always maps to equal or higher privacy requirement

## Example Calculations

### Example 1: Low Risk Token

```python
sniper_score = 0.2
volatility = 0.3
velocity = 0.4
liquidity_depth = 0.7

liquidity_risk_inv = 1.0 - 0.7 = 0.3
velocity_norm = min(1.0, 0.4 * 1.2) = 0.48

risk_score = (
    0.35 * 0.2 +
    0.25 * 0.3 +
    0.20 * 0.48 +
    0.20 * 0.3
) = 0.07 + 0.075 + 0.096 + 0.06 = 0.301

risk_level = "low"  # 0.301 < 0.35
```

### Example 2: High Risk Token

```python
sniper_score = 0.8
volatility = 0.7
velocity = 0.9
liquidity_depth = 0.2

liquidity_risk_inv = 1.0 - 0.2 = 0.8
velocity_norm = min(1.0, 0.9 * 1.2) = 1.0

risk_score = (
    0.35 * 0.8 +
    0.25 * 0.7 +
    0.20 * 1.0 +
    0.20 * 0.8
) = 0.28 + 0.175 + 0.2 + 0.16 = 0.815

risk_level = "high"  # 0.7 <= 0.815 < 0.9
```

### Example 3: Critical Risk Token

```python
sniper_score = 0.95
volatility = 0.9
velocity = 1.0
liquidity_depth = 0.1

liquidity_risk_inv = 1.0 - 0.1 = 0.9
velocity_norm = min(1.0, 1.0 * 1.2) = 1.0

risk_score = (
    0.35 * 0.95 +
    0.25 * 0.9 +
    0.20 * 1.0 +
    0.20 * 0.9
) = 0.3325 + 0.225 + 0.2 + 0.18 = 0.9375

risk_level = "critical"  # 0.9375 >= 0.9
```

## Configuration

### Environment Variables

```bash
HIGH_RISK_THRESHOLD=0.7      # Threshold for high risk
CRITICAL_RISK_THRESHOLD=0.9  # Threshold for critical risk
```

### Weights (Current v0.1)

```python
SNIPER_WEIGHT = 0.35
VOLATILITY_WEIGHT = 0.25
VELOCITY_WEIGHT = 0.20
LIQUIDITY_WEIGHT = 0.20
```

**Note**: Weights sum to 1.0. Adjustments should maintain this constraint.

## Future Improvements

- **Adaptive Weights**: Adjust weights based on market conditions
- **Machine Learning**: Train model on historical outcomes
- **Multi-factor Models**: Add more factors (whale activity, bot patterns, etc.)
- **Time-decay**: Weight recent data more heavily
- **Cross-token Analysis**: Consider correlation with other tokens

