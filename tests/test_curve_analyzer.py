"""
Tests for curve analyzer
"""

import pytest
from solders.pubkey import Pubkey
from src.curve_intelligence.curve_analyzer import CurveAnalyzer


@pytest.mark.asyncio
async def test_curve_analyzer_init():
    """Test curve analyzer initialization"""
    analyzer = CurveAnalyzer()
    assert analyzer.cache == {}


@pytest.mark.asyncio
async def test_analyze_curve():
    """Test curve analysis"""
    analyzer = CurveAnalyzer()
    token_mint = Pubkey.from_string("11111111111111111111111111111111")
    
    curve_data = {
        "current_price": 0.001,
        "slope": 0.5,
        "liquidity": 100.0,
        "total_supply": 1000000.0,
        "market_cap": 1000.0
    }
    
    analysis = await analyzer.analyze_curve(token_mint, curve_data)
    
    assert analysis["token_mint"] == str(token_mint)
    assert "slope_position" in analysis
    assert "liquidity_depth" in analysis
    assert "volatility" in analysis


def test_calculate_slope_position():
    """Test slope position calculation"""
    analyzer = CurveAnalyzer()
    
    position = analyzer._calculate_slope_position(0.5, 0.001)
    assert 0.0 <= position <= 1.0


def test_calculate_liquidity_depth():
    """Test liquidity depth calculation"""
    analyzer = CurveAnalyzer()
    
    depth = analyzer._calculate_liquidity_depth(100.0, 1000.0)
    assert 0.0 <= depth <= 1.0


def test_get_cached_analysis():
    """Test getting cached analysis"""
    analyzer = CurveAnalyzer()
    token_mint = Pubkey.from_string("11111111111111111111111111111111")
    
    # No cache yet
    assert analyzer.get_cached_analysis(token_mint) is None
    
    # Add to cache manually
    analyzer.cache[str(token_mint)] = {"test": "data"}
    assert analyzer.get_cached_analysis(token_mint) is not None

