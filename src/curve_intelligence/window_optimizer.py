"""
Window Optimizer

Calculates optimal execution windows for transactions.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from solders.pubkey import Pubkey
from .risk_detector import RiskDetector, RiskLevel
from .curve_analyzer import CurveAnalyzer
from ..utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class ExecutionWindow:
    """
    Execution window data structure
    
    Attributes:
        start_time: Window start time
        end_time: Window end time
        risk_level: Risk level in window
        expected_slippage: Expected slippage percentage
        sniper_activity: Sniper activity level (0.0 to 1.0)
        confidence: Confidence score (0.0 to 1.0)
        optimal_time: Optimal execution time within window
    """
    start_time: datetime
    end_time: datetime
    risk_level: RiskLevel
    expected_slippage: float
    sniper_activity: float
    confidence: float
    optimal_time: Optional[datetime] = None


class WindowOptimizer:
    """
    Optimizes execution windows for transactions
    """
    
    def __init__(
        self,
        risk_detector: Optional[RiskDetector] = None,
        curve_analyzer: Optional[CurveAnalyzer] = None
    ):
        """
        Initialize window optimizer
        
        Args:
            risk_detector: Risk detector instance
            curve_analyzer: Curve analyzer instance
        """
        self.risk_detector = risk_detector or RiskDetector()
        self.curve_analyzer = curve_analyzer or CurveAnalyzer()
        logger.info("WindowOptimizer initialized")
    
    async def get_optimal_window(
        self,
        token_mint: Pubkey,
        intent: str,  # "buy" or "sell"
        amount: float,
        max_wait_minutes: int = 30
    ) -> ExecutionWindow:
        """
        Calculate optimal execution window
        
        Args:
            token_mint: Token mint address
            intent: Transaction intent ("buy" or "sell")
            amount: Transaction amount
            max_wait_minutes: Maximum time to wait for window
            
        Returns:
            ExecutionWindow instance
        """
        # Get risk assessment
        risk_assessment = await self.risk_detector.assess_risk(token_mint)
        
        # Get curve analysis
        curve_analysis = await self.curve_analyzer.analyze_curve(token_mint)
        
        # Calculate optimal window
        window = self._calculate_window(
            risk_assessment,
            curve_analysis,
            intent,
            amount,
            max_wait_minutes
        )
        
        logger.info(
            f"Optimal window for {token_mint} ({intent}): "
            f"risk={window.risk_level.value}, confidence={window.confidence:.2f}"
        )
        
        return window
    
    def _calculate_window(
        self,
        risk_assessment: Dict[str, Any],
        curve_analysis: Dict[str, Any],
        intent: str,
        amount: float,
        max_wait: int
    ) -> ExecutionWindow:
        """
        Calculate execution window based on risk and curve data
        
        Args:
            risk_assessment: Risk assessment results
            curve_analysis: Curve analysis results
            intent: Transaction intent
            amount: Transaction amount
            max_wait: Maximum wait time in minutes
            
        Returns:
            ExecutionWindow instance
        """
        now = datetime.utcnow()
        
        # Get risk level
        overall_risk_str = risk_assessment.get("overall_risk", "medium")
        try:
            risk_level = RiskLevel(overall_risk_str)
        except ValueError:
            risk_level = RiskLevel.MEDIUM
        
        # Get sniper activity
        sniper_result = risk_assessment.get("sniper_activity", {})
        sniper_prob = sniper_result.get("probability", 0.5)
        
        # Calculate window duration based on risk
        if risk_level == RiskLevel.CRITICAL:
            window_duration = timedelta(minutes=5)  # Short window, high risk
            wait_time = timedelta(minutes=min(10, max_wait))
        elif risk_level == RiskLevel.HIGH:
            window_duration = timedelta(minutes=10)
            wait_time = timedelta(minutes=min(15, max_wait))
        elif risk_level == RiskLevel.MEDIUM:
            window_duration = timedelta(minutes=15)
            wait_time = timedelta(minutes=min(20, max_wait))
        else:  # LOW
            window_duration = timedelta(minutes=20)
            wait_time = timedelta(minutes=min(30, max_wait))
        
        # Calculate expected slippage
        volatility = curve_analysis.get("volatility", 0.5)
        liquidity_depth = curve_analysis.get("liquidity_depth", 0.5)
        
        # Higher volatility and lower liquidity = higher slippage
        expected_slippage = (volatility * 0.6 + (1 - liquidity_depth) * 0.4) * 0.1  # Max 10%
        
        # Calculate confidence
        # Lower risk and better conditions = higher confidence
        risk_score = {
            RiskLevel.LOW: 0.9,
            RiskLevel.MEDIUM: 0.7,
            RiskLevel.HIGH: 0.5,
            RiskLevel.CRITICAL: 0.3
        }[risk_level]
        
        confidence = risk_score * (1 - sniper_prob * 0.3)  # Reduce confidence if snipers active
        
        # Optimal time is start of window (can be adjusted)
        start_time = now + wait_time
        end_time = start_time + window_duration
        optimal_time = start_time + (window_duration / 2)  # Middle of window
        
        return ExecutionWindow(
            start_time=start_time,
            end_time=end_time,
            risk_level=risk_level,
            expected_slippage=expected_slippage,
            sniper_activity=sniper_prob,
            confidence=confidence,
            optimal_time=optimal_time
        )
    
    async def assess_trade_impact(
        self,
        token_mint: Pubkey,
        amount: float,
        trade_type: str  # "buy" or "sell"
    ) -> Dict[str, Any]:
        """
        Assess impact of a trade on the curve
        
        Args:
            token_mint: Token mint address
            amount: Trade amount
            trade_type: Type of trade
            
        Returns:
            Dictionary with impact assessment
        """
        # Get curve analysis
        curve_analysis = await self.curve_analyzer.analyze_curve(token_mint)
        
        liquidity = curve_analysis.get("liquidity", 0.0)
        current_price = curve_analysis.get("current_price", 0.0)
        
        # Calculate price impact
        if liquidity > 0:
            # Simplified impact calculation
            # Real implementation would use actual curve formula
            impact_ratio = amount / liquidity
            price_impact = impact_ratio * current_price * 0.1  # Simplified
        else:
            price_impact = current_price * 0.5  # High impact if no liquidity
        
        # Estimate slippage
        slippage = min(0.1, price_impact / current_price) if current_price > 0 else 0.1
        
        return {
            "token_mint": str(token_mint),
            "trade_type": trade_type,
            "amount": amount,
            "estimated_price_impact": price_impact,
            "estimated_slippage": slippage,
            "liquidity_after": max(0, liquidity - amount) if trade_type == "buy" else liquidity + amount
        }

