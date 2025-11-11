"""
Curve Intelligence Layer

Main interface that coordinates all curve intelligence components.
"""

from typing import Optional, Dict, Any
from solders.pubkey import Pubkey
from .curve_analyzer import CurveAnalyzer
from .risk_detector import RiskDetector
from .window_optimizer import WindowOptimizer, ExecutionWindow
from .pattern_recognition import PatternRecognizer
from ..data.collectors import DataCollector
from ..utils.logger import get_logger

logger = get_logger(__name__)


class CurveIntelligenceLayer:
    """
    Main interface for curve intelligence
    
    Coordinates curve analysis, risk detection, window optimization,
    and pattern recognition.
    """
    
    def __init__(
        self,
        rpc_url: str = "https://api.mainnet-beta.solana.com",
        data_collector: Optional[DataCollector] = None
    ):
        """
        Initialize curve intelligence layer
        
        Args:
            rpc_url: Solana RPC endpoint
            data_collector: Optional data collector instance
        """
        self.data_collector = data_collector or DataCollector(rpc_url=rpc_url)
        self.curve_analyzer = CurveAnalyzer(data_collector=self.data_collector)
        self.risk_detector = RiskDetector(data_collector=self.data_collector)
        self.window_optimizer = WindowOptimizer(
            risk_detector=self.risk_detector,
            curve_analyzer=self.curve_analyzer
        )
        self.pattern_recognizer = PatternRecognizer(data_collector=self.data_collector)
        
        logger.info("CurveIntelligenceLayer initialized")
    
    async def analyze_token(
        self,
        token_mint: Pubkey
    ) -> Dict[str, Any]:
        """
        Comprehensive token analysis
        
        Args:
            token_mint: Token mint address
            
        Returns:
            Dictionary with complete analysis
        """
        # Get curve analysis
        curve_analysis = await self.curve_analyzer.analyze_curve(token_mint)
        
        # Get risk assessment
        risk_assessment = await self.risk_detector.assess_risk(token_mint, curve_analysis)
        
        # Detect patterns
        patterns = await self.pattern_recognizer.detect_patterns(token_mint)
        
        # Compile comprehensive analysis
        analysis = {
            "token_mint": str(token_mint),
            "curve_analysis": curve_analysis,
            "risk_assessment": risk_assessment,
            "patterns": patterns,
            "timestamp": curve_analysis.get("timestamp")
        }
        
        logger.info(f"Comprehensive analysis completed for {token_mint}")
        
        return analysis
    
    async def get_optimal_window(
        self,
        token_mint: Pubkey,
        intent: str,  # "buy" or "sell"
        amount: float
    ) -> ExecutionWindow:
        """
        Get optimal execution window
        
        Args:
            token_mint: Token mint address
            intent: Transaction intent
            amount: Transaction amount
            
        Returns:
            ExecutionWindow instance
        """
        return await self.window_optimizer.get_optimal_window(
            token_mint,
            intent,
            amount
        )
    
    async def assess_risk(
        self,
        token_mint: Pubkey
    ) -> Dict[str, Any]:
        """
        Assess risk for a token
        
        Args:
            token_mint: Token mint address
            
        Returns:
            Risk assessment dictionary
        """
        return await self.risk_detector.assess_risk(token_mint)
    
    async def detect_sniper_window(
        self,
        token_mint: Pubkey,
        time_window_minutes: int = 5
    ) -> Dict[str, Any]:
        """
        Detect sniper activity window
        
        Args:
            token_mint: Token mint address
            time_window_minutes: Time window to analyze
            
        Returns:
            Sniper detection results
        """
        return await self.risk_detector.detect_sniper_window(
            token_mint,
            time_window_minutes
        )
    
    async def detect_patterns(
        self,
        token_mint: Pubkey,
        time_window_minutes: int = 30
    ) -> list:
        """
        Detect trading patterns
        
        Args:
            token_mint: Token mint address
            time_window_minutes: Time window to analyze
            
        Returns:
            List of detected patterns
        """
        return await self.pattern_recognizer.detect_patterns(
            token_mint,
            time_window_minutes
        )
    
    async def assess_trade_impact(
        self,
        token_mint: Pubkey,
        amount: float,
        trade_type: str
    ) -> Dict[str, Any]:
        """
        Assess trade impact on curve
        
        Args:
            token_mint: Token mint address
            amount: Trade amount
            trade_type: "buy" or "sell"
            
        Returns:
            Trade impact assessment
        """
        return await self.window_optimizer.assess_trade_impact(
            token_mint,
            amount,
            trade_type
        )
    
    async def close(self):
        """Close connections and cleanup"""
        await self.data_collector.disconnect()
        logger.info("CurveIntelligenceLayer closed")

