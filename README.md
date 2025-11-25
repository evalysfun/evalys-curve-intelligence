# Evalys Curve Intelligence

Real-time curve analysis, risk detection, and execution window optimization for memecoin launchpads.

## 🎯 Overview

The Curve Intelligence Layer provides:
- 📊 **Real-time Curve Analysis**: Analyze bonding curves in real-time
- 🛡️ **Risk Detection**: Detect snipers, buy clusters, and liquidity risks
- ⏰ **Window Optimization**: Calculate optimal execution windows
- 🔍 **Pattern Recognition**: Detect whales, bots, and anomalies

## ✨ Features

- 📈 **Curve Analysis**: Slope position, liquidity depth, volatility
- 🎯 **Sniper Detection**: Identify when snipers are active
- 📦 **Buy Cluster Detection**: Find grouped transactions
- ⚡ **Execution Windows**: Optimal timing for transactions
- 🐋 **Pattern Recognition**: Whales, bots, pump/dump patterns
- 🌐 **REST API**: Full API for integration
- 📦 **Standalone**: Can be used independently

## 🚀 Installation

### From Source (Recommended: Shared Virtual Environment)

For the Evalys ecosystem, use a **shared virtual environment** at the root level:

```bash
# From evalys root directory (if not already set up)
venv\Scripts\Activate.ps1  # Windows PowerShell
$env:PYTHONPATH = "."

# Navigate to component directory
cd evalys-curve-intelligence

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

**Note**: Using a shared venv at the root avoids duplication. All Evalys components share the same environment.

### Standalone Installation

If using this component independently:

```bash
git clone https://github.com/evalysfun/evalys-curve-intelligence
cd evalys-curve-intelligence
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
pip install -e .
```

## 📖 Usage

### As Python Library

```python
import asyncio
from solders.pubkey import Pubkey
from src.curve_intelligence.intelligence_layer import CurveIntelligenceLayer

async def main():
    # Initialize intelligence layer
    intelligence = CurveIntelligenceLayer(rpc_url="https://api.devnet.solana.com")
    
    try:
        token_mint = Pubkey.from_string("...")
        
        # Comprehensive analysis
        analysis = await intelligence.analyze_token(token_mint)
        
        # Get optimal execution window
        window = await intelligence.get_optimal_window(
            token_mint,
            intent="buy",
            amount=1.0
        )
        
        # Assess risk
        risk = await intelligence.assess_risk(token_mint)
        
        # Detect patterns
        patterns = await intelligence.detect_patterns(token_mint)
        
    finally:
        await intelligence.close()

asyncio.run(main())
```

### As REST API

```bash
# Start the API server
python -m src.api.server

# Or use uvicorn directly
uvicorn src.api.server:app --host 0.0.0.0 --port 8003
```

#### API Endpoints

- `POST /api/v1/curve/analyze` - Comprehensive token analysis
- `POST /api/v1/curve/optimal-window` - Get optimal execution window
- `GET /api/v1/curve/risk/{token_mint}` - Get risk assessment
- `GET /api/v1/curve/sniper/{token_mint}` - Detect sniper activity
- `GET /api/v1/curve/patterns/{token_mint}` - Get detected patterns
- `POST /api/v1/curve/trade-impact` - Assess trade impact
- `GET /health` - Health check

#### Example API Request

```bash
# Get risk assessment
curl "http://localhost:8003/api/v1/curve/risk/TOKEN_MINT"

# Get optimal window
curl -X POST "http://localhost:8003/api/v1/curve/optimal-window" \
  -H "Content-Type: application/json" \
  -d '{
    "token_mint": "TOKEN_MINT",
    "intent": "buy",
    "amount": 1.0
  }'
```

## 🏗️ Architecture

```
Curve Intelligence Layer
├── Curve Analyzer      # Curve data analysis (slope, depth, velocity, volatility)
├── Risk Detector       # Risk assessment (sniper, clusters, liquidity)
├── Window Optimizer    # Execution window calculation
├── Pattern Recognizer  # Pattern detection (whales, bots, pump/dump)
└── Data Collector      # Data collection (RPC, on-chain parsing)
```

**Analysis Pipeline**:
1. Fetch recent transactions and curve state
2. Calculate core metrics (slope, depth, velocity, volatility)
3. Run detection algorithms (sniper, clusters, patterns)
4. Calculate risk score using weighted formula
5. Determine optimal execution window
6. Return comprehensive analysis

## 🔧 Configuration

Set environment variables:

```bash
export SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
export DEFAULT_TIME_WINDOW_MINUTES=30
export SNIPER_DETECTION_WINDOW=5
export HIGH_RISK_THRESHOLD=0.7
export API_HOST=0.0.0.0
export API_PORT=8003
```

## 🧪 Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=src --cov-report=html
```

### Demo

Run the interactive demo:

```bash
python examples/demo.py
```

This demonstrates:
- Curve metrics calculation
- Sniper detection
- Buy cluster detection
- Risk assessment
- Pattern recognition
- Optimal window calculation

Perfect for screen recordings and promotional videos.

**Expected Output**: See `examples/demo.py` for full demonstration of all features.

## 📦 Project Structure

```
evalys-curve-intelligence/
├── src/
│   ├── curve_intelligence/  # Core intelligence logic
│   │   ├── curve_analyzer.py
│   │   ├── risk_detector.py
│   │   ├── window_optimizer.py
│   │   ├── pattern_recognition.py
│   │   └── intelligence_layer.py
│   ├── data/                # Data collection
│   ├── api/                 # REST API
│   ├── config/              # Configuration
│   └── utils/               # Utilities
├── docs/
│   ├── curve-spec.md        # Curve analysis specification
│   ├── detection.md          # Detection algorithms
│   ├── risk-model.md         # Risk calculation formula
│   └── evaluation.md         # Evaluation results
├── examples/
│   └── demo.py              # Runnable demo script
├── tests/                   # Tests
├── CHANGELOG.md
├── ROADMAP.md
├── requirements.txt
├── setup.py
└── README.md
```

## 📝 Implementation Status

### Implemented (v0.1)

- ✅ **Curve Analysis**: Slope, liquidity depth, trade velocity, volatility calculations
- ✅ **Sniper Detection**: Algorithm v0.1 with frequency, interval, and pattern analysis
- ✅ **Buy Cluster Detection**: Time-based clustering with wallet correlation
- ✅ **Risk Assessment**: Weighted risk formula with configurable thresholds
- ✅ **Pattern Recognition**: Basic whale, bot, pump/dump pattern detection
- ✅ **Window Optimization**: Optimal execution window calculation
- ✅ **REST API**: Full FastAPI with all endpoints
- ✅ **Python Library**: Standalone library interface
- ✅ **Documentation**: Comprehensive specs, algorithms, and evaluation results
- ✅ **Tests**: Basic test suite

### Planned

- ⏳ **Full On-Chain Data Fetching**: Complete implementation of RPC data collection
- ⏳ **Machine Learning Models**: Trained models for pattern recognition
- ⏳ **Real-Time WebSocket Updates**: Live data streaming
- ⏳ **Indexer Integration**: Helius, QuickNode integration
- ⏳ **Advanced Pattern Recognition**: Multi-wallet correlation, cross-token analysis
- ⏳ **Adaptive Thresholds**: Market-condition-based threshold adjustment
- ⏳ **Historical Backtesting**: Backtesting framework for validation

**Note**: The intelligence layer provides the framework and algorithms. On-chain data fetching is partially implemented and needs completion based on launchpad program structures.

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines first.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Related Projects

- [evalys-privacy-engine](https://github.com/evalysfun/evalys-privacy-engine) - Privacy mode orchestration
- [evalys-burner-swarm](https://github.com/evalysfun/evalys-burner-swarm) - Burner wallet management
- [evalys-launchpad-adapters](https://github.com/evalysfun/evalys-launchpad-adapters) - Launchpad integrations
- [evalys-execution-engine](https://github.com/evalysfun/evalys-execution-engine) - Transaction execution

## 📚 Documentation

- **[Curve Spec](docs/curve-spec.md)**: Data sources, metrics, output schema
- **[Detection Algorithms](docs/detection.md)**: Sniper and cluster detection algorithms
- **[Risk Model](docs/risk-model.md)**: Risk calculation formula and thresholds
- **[Evaluation](docs/evaluation.md)**: Test results and accuracy metrics
- **[Changelog](CHANGELOG.md)**: Version history
- **[Roadmap](ROADMAP.md)**: Planned features and improvements

## 📊 Measurable Behavior

Instead of vague claims, here's what the system actually does:

**Sniper Detection**:
- Analyzes transaction frequency, intervals, and wallet patterns
- Calculates sniper score: `[0, 1]` based on frequency, interval, first-seen ratio, price impact
- Threshold: `sniper_score >= 0.6` AND `transaction_count >= 5` = active

**Buy Cluster Detection**:
- Groups transactions by time windows (60s clusters)
- Analyzes wallet correlation and size similarity
- Returns clusters with correlation scores: `[0, 1]`

**Risk Assessment**:
- Formula: `0.35 * sniper_score + 0.25 * volatility + 0.20 * velocity + 0.20 * liquidity_risk`
- Thresholds: Low < 0.35, Medium 0.35-0.7, High 0.7-0.9, Critical >= 0.9
- Maps to privacy mode recommendations

**Curve Metrics**:
- Slope: Rate of price change per supply unit (normalized [0, 1])
- Liquidity Depth: Available liquidity at current price (normalized [0, 1])
- Trade Velocity: Transactions per second (normalized [0, 1])
- Volatility: Price volatility over rolling window (normalized [0, 1])

See [Curve Spec](docs/curve-spec.md) and [Detection Algorithms](docs/detection.md) for detailed specifications.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/evalysfun/evalys-curve-intelligence/issues)
- **Documentation**: See `docs/` directory
- **Related Projects**: See below

## 🔗 Related Projects

- [evalys-privacy-engine](https://github.com/evalysfun/evalys-privacy-engine) - Privacy mode orchestration
- [evalys-burner-swarm](https://github.com/evalysfun/evalys-burner-swarm) - Burner wallet management
- [evalys-launchpad-adapters](https://github.com/evalysfun/evalys-launchpad-adapters) - Launchpad integrations
- [evalys-execution-engine](https://github.com/evalysfun/evalys-execution-engine) - Transaction execution

---

**Evalys Curve Intelligence** - Real-time analysis with measurable algorithms 📊

