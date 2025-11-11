"""
API Routes for Curve Intelligence

REST API endpoints for curve analysis and intelligence.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from solders.pubkey import Pubkey
from ..curve_intelligence.intelligence_layer import CurveIntelligenceLayer
from ..config.settings import Settings

router = APIRouter(prefix="/api/v1/curve", tags=["curve"])

# Global intelligence layer (in production, use dependency injection)
intelligence = CurveIntelligenceLayer(rpc_url=Settings.SOLANA_RPC_URL)


class AnalyzeTokenRequest(BaseModel):
    """Request model for token analysis"""
    token_mint: str = Field(..., description="Token mint address")


class GetOptimalWindowRequest(BaseModel):
    """Request model for optimal window"""
    token_mint: str = Field(..., description="Token mint address")
    intent: str = Field(..., description="Transaction intent: 'buy' or 'sell'")
    amount: float = Field(..., ge=0.0, description="Transaction amount")


class AssessTradeImpactRequest(BaseModel):
    """Request model for trade impact assessment"""
    token_mint: str = Field(..., description="Token mint address")
    amount: float = Field(..., ge=0.0, description="Trade amount")
    trade_type: str = Field(..., description="Trade type: 'buy' or 'sell'")


@router.post("/analyze")
async def analyze_token(request: AnalyzeTokenRequest):
    """
    Comprehensive token analysis
    
    Returns curve analysis, risk assessment, and patterns.
    """
    try:
        token_mint = Pubkey.from_string(request.token_mint)
        analysis = await intelligence.analyze_token(token_mint)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/optimal-window")
async def get_optimal_window(request: GetOptimalWindowRequest):
    """
    Get optimal execution window
    
    Returns the best time window for executing a transaction.
    """
    try:
        token_mint = Pubkey.from_string(request.token_mint)
        
        if request.intent not in ["buy", "sell"]:
            raise HTTPException(status_code=400, detail="intent must be 'buy' or 'sell'")
        
        window = await intelligence.get_optimal_window(
            token_mint,
            request.intent,
            request.amount
        )
        
        return {
            "token_mint": request.token_mint,
            "intent": request.intent,
            "amount": request.amount,
            "start_time": window.start_time.isoformat(),
            "end_time": window.end_time.isoformat(),
            "optimal_time": window.optimal_time.isoformat() if window.optimal_time else None,
            "risk_level": window.risk_level.value,
            "expected_slippage": window.expected_slippage,
            "sniper_activity": window.sniper_activity,
            "confidence": window.confidence
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/risk/{token_mint}")
async def get_risk_assessment(token_mint: str):
    """Get risk assessment for a token"""
    try:
        mint = Pubkey.from_string(token_mint)
        assessment = await intelligence.assess_risk(mint)
        return assessment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sniper/{token_mint}")
async def detect_sniper(token_mint: str, time_window: int = 5):
    """Detect sniper activity"""
    try:
        mint = Pubkey.from_string(token_mint)
        result = await intelligence.detect_sniper_window(mint, time_window)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/patterns/{token_mint}")
async def get_patterns(token_mint: str, time_window: int = 30):
    """Get detected patterns"""
    try:
        mint = Pubkey.from_string(token_mint)
        patterns = await intelligence.detect_patterns(mint, time_window)
        return {
            "token_mint": token_mint,
            "patterns": patterns,
            "count": len(patterns)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/trade-impact")
async def assess_trade_impact(request: AssessTradeImpactRequest):
    """Assess trade impact on curve"""
    try:
        token_mint = Pubkey.from_string(request.token_mint)
        
        if request.trade_type not in ["buy", "sell"]:
            raise HTTPException(status_code=400, detail="trade_type must be 'buy' or 'sell'")
        
        impact = await intelligence.assess_trade_impact(
            token_mint,
            request.amount,
            request.trade_type
        )
        
        return impact
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

