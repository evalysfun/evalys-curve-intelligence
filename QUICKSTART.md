# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Setup Shared Virtual Environment (Recommended)

Since Evalys uses multiple components, use a **shared virtual environment** at the root level:

```bash
# From evalys root directory (if not already set up)
venv\Scripts\Activate.ps1  # Windows PowerShell
$env:PYTHONPATH = "."

# Navigate to curve intelligence directory
cd evalys-curve-intelligence

# Install dependencies
pip install -r requirements.txt
```

**Note**: The shared venv approach avoids duplication. All Evalys components share the same environment.

### 2. Run Example

```bash
# Make sure you're in evalys-curve-intelligence directory
# and venv is activated with PYTHONPATH set
python example.py
```

This will demonstrate the curve intelligence features.

### 3. Use as Python Library

```python
import asyncio
from src.curve_intelligence.intelligence_layer import CurveIntelligenceLayer
from solders.pubkey import Pubkey

async def main():
    intelligence = CurveIntelligenceLayer(rpc_url="https://api.devnet.solana.com")
    
    try:
        token_mint = Pubkey.from_string("...")
        
        # Analyze token
        analysis = await intelligence.analyze_token(token_mint)
        
        # Get optimal window
        window = await intelligence.get_optimal_window(token_mint, "buy", 1.0)
    finally:
        await intelligence.close()

asyncio.run(main())
```

### 4. Run as API Server

```bash
# Start the API server
python -m src.api.server

# Or use uvicorn directly
uvicorn src.api.server:app --host 0.0.0.0 --port 8003 --reload
```

Then visit:
- API Docs: http://localhost:8003/docs
- Health Check: http://localhost:8003/health

### 5. Test API

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

### 6. Run Tests

```bash
# Install test dependencies (if not already installed)
pip install pytest pytest-asyncio pytest-cov

# Run tests
pytest

# With coverage
pytest --cov=src --cov-report=html
```

## 📚 Next Steps

- Read the [README.md](README.md) for detailed documentation
- Check out the [example.py](example.py) for more usage examples
- Explore the API at http://localhost:8003/docs when server is running

## 🐛 Troubleshooting

### Import Errors
Make sure:
1. Virtual environment is activated
2. PYTHONPATH is set (see step 1)
3. You're in the evalys-curve-intelligence directory

### Data Collection Issues
The data collector provides the framework. Actual on-chain data fetching needs to be implemented based on launchpad program structures.

### Module Not Found
Make sure:
1. Virtual environment is activated
2. PYTHONPATH is set (see step 1)
3. You're in the evalys-curve-intelligence directory

```bash
# Verify PYTHONPATH is set
echo $env:PYTHONPATH  # Windows PowerShell
# or
echo $PYTHONPATH      # Linux/Mac

# Run from component directory
python -m src.api.server
```

