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
        data_collector: Optional[DataCollector] = None,
        use_confidential_intel: bool = False,
    ):
        """
        Initialize curve intelligence layer
        
        Args:
            rpc_url: Solana RPC endpoint
            data_collector: Optional data collector instance
            use_confidential_intel: Whether to use Arcium confidential intelligence
        """
        self.data_collector = data_collector or DataCollector(rpc_url=rpc_url)
        self.curve_analyzer = CurveAnalyzer(data_collector=self.data_collector)
        self.risk_detector = RiskDetector(data_collector=self.data_collector)
        self.window_optimizer = WindowOptimizer(
            risk_detector=self.risk_detector,
            curve_analyzer=self.curve_analyzer
        )
        self.pattern_recognizer = PatternRecognizer(data_collector=self.data_collector)
        self.use_confidential_intel = use_confidential_intel
        self._arcium_client = None
        
        logger.info(f"CurveIntelligenceLayer initialized (confidential_intel: {use_confidential_intel})")
    
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
    
    def _get_arcium_client(self):
        """Lazy import of Arcium bridge client"""
        if self._arcium_client is None and self.use_confidential_intel:
            try:
                import sys
                import os
                bridge_path = os.path.join(
                    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
                    "evalys-arcium-bridge-service", "src"
                )
                if os.path.exists(bridge_path):
                    sys.path.insert(0, os.path.dirname(bridge_path))
                    from bridge.arcium_client import ArciumBridgeClient
                    from bridge.models import SizingPreferences, UserConstraints, CurveMetrics
                    self._arcium_client = {
                        "client": ArciumBridgeClient,
                        "models": {
                            "SizingPreferences": SizingPreferences,
                            "UserConstraints": UserConstraints,
                            "CurveMetrics": CurveMetrics,
                        }
                    }
            except ImportError:
                logger.warning("Arcium bridge service not available for confidential intel")
                self._arcium_client = False
        return self._arcium_client
    
    async def get_confidential_curve_evaluation(
        self,
        token_mint: Pubkey,
        sizing_preferences: Dict[str, Any],
        user_constraints: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        """
        Get confidential curve evaluation using Arcium
        
        Args:
            token_mint: Token mint address
            sizing_preferences: Encrypted sizing preferences
            user_constraints: Encrypted user constraints
            
        Returns:
            Confidential execution recommendation or None if Arcium unavailable
        """
        if not self.use_confidential_intel:
            return None
        
        arcium_client_info = self._get_arcium_client()
        if not arcium_client_info:
            logger.warning("Arcium client not available for confidential curve evaluation")
            return None
        
        try:
            # Get public curve metrics
            curve_analysis = await self.curve_analyzer.analyze_curve(token_mint)
            
            # Build curve metrics from analysis
            curve_metrics = {
                "current_price": int(curve_analysis.get("current_price", 0)),
                "price_change_24h": int(curve_analysis.get("price_change_24h", 0)),
                "liquidity_depth": int(curve_analysis.get("liquidity_depth", 0)),
                "buy_pressure": int(curve_analysis.get("buy_pressure", 0)),
                "sell_pressure": int(curve_analysis.get("sell_pressure", 0)),
            }
            
            # Build models
            client_class = arcium_client_info["client"]
            models = arcium_client_info["models"]
            
            client = client_class()
            
            sizing = models["SizingPreferences"](**sizing_preferences)
            constraints = models["UserConstraints"](**user_constraints)
            metrics = models["CurveMetrics"](**curve_metrics)
            
            # Get confidential evaluation
            recommendation = await client.get_curve_evaluation(
                sizing_preferences=sizing,
                user_constraints=constraints,
                curve_metrics=metrics,
            )
            
            await client.close()
            
            logger.info(f"Received confidential curve evaluation for {token_mint}")
            
            return {
                "recommended_size": recommendation.recommended_size,
                "entry_price_target": recommendation.entry_price_target,
                "execution_urgency": recommendation.execution_urgency,
                "optimal_timing": recommendation.optimal_timing,
                "confidence_score": recommendation.confidence_score,
            }
        except Exception as e:
            logger.error(f"Error getting confidential curve evaluation: {e}")
            return None
    
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

