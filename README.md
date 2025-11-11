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
├── Curve Analyzer      # Curve data analysis
├── Risk Detector       # Risk assessment
├── Window Optimizer    # Execution window calculation
├── Pattern Recognizer  # Pattern detection
└── Data Collector      # Data collection
```

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
├── tests/                   # Tests
├── requirements.txt
├── setup.py
└── README.md
```

## 📝 Implementation Status

- ✅ Framework structure
- ✅ Curve analysis logic
- ✅ Risk detection algorithms
- ✅ Window optimization
- ✅ Pattern recognition
- ⚠️ On-chain data fetching (needs implementation)
- ⚠️ Real transaction history (needs implementation)

**Note**: The intelligence layer provides the framework and algorithms. Actual on-chain data fetching needs to be implemented based on launchpad program structures.

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

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/evalysfun/evalys-curve-intelligence/issues)
- **Discord**: [Coming Soon]

---

**Evalys Curve Intelligence** - Real-time analysis for memecoin launchpads 📊

