"""
Curve Analyzer

Analyzes bonding curve data in real-time.
"""

from typing import Optional, Dict, Any
from solders.pubkey import Pubkey
from datetime import datetime
from ..data.collectors import DataCollector
from ..utils.logger import get_logger

logger = get_logger(__name__)


class CurveAnalyzer:
    """
    Analyzes bonding curve data
    """
    
    def __init__(self, data_collector: Optional[DataCollector] = None):
        """
        Initialize curve analyzer
        
        Args:
            data_collector: Data collector instance
        """
        self.data_collector = data_collector
        self.cache: Dict[str, Dict[str, Any]] = {}
        logger.info("CurveAnalyzer initialized")
    
    async def analyze_curve(
        self,
        token_mint: Pubkey,
        curve_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze bonding curve
        
        Args:
            token_mint: Token mint address
            curve_data: Optional curve data (fetches if not provided)
            
        Returns:
            Dictionary with analysis results
        """
        if curve_data is None and self.data_collector:
            curve_data = await self.data_collector.get_curve_data(token_mint)
        
        if not curve_data:
            raise ValueError("No curve data available")
        
        # Calculate metrics
        current_price = curve_data.get("current_price", 0.0)
        slope = curve_data.get("slope", 0.0)
        liquidity = curve_data.get("liquidity", 0.0)
        total_supply = curve_data.get("total_supply", 0.0)
        market_cap = curve_data.get("market_cap", 0.0)
        
        # Calculate slope position (where on the curve)
        slope_position = self._calculate_slope_position(slope, current_price)
        
        # Calculate liquidity depth
        liquidity_depth = self._calculate_liquidity_depth(liquidity, market_cap)
        
        # Calculate volatility
        volatility = self._calculate_volatility(curve_data)
        
        analysis = {
            "token_mint": str(token_mint),
            "current_price": current_price,
            "slope": slope,
            "slope_position": slope_position,  # 0.0 to 1.0
            "liquidity": liquidity,
            "liquidity_depth": liquidity_depth,  # 0.0 to 1.0
            "total_supply": total_supply,
            "market_cap": market_cap,
            "volatility": volatility,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Cache analysis
        self.cache[str(token_mint)] = analysis
        
        logger.debug(f"Analyzed curve for {token_mint}: position={slope_position:.2f}, depth={liquidity_depth:.2f}")
        
        return analysis
    
    def _calculate_slope_position(self, slope: float, price: float) -> float:
        """
        Calculate position on the curve (0.0 = early, 1.0 = late)
        
        Args:
            slope: Curve slope
            price: Current price
            
        Returns:
            Position value (0.0 to 1.0)
        """
        # Simplified calculation
        # Real implementation would use actual curve parameters
        if slope == 0:
            return 0.5
        
        # Normalize based on slope and price
        # Higher price + steeper slope = later position
        normalized = min(1.0, max(0.0, (price * slope) / 1000.0))
        return normalized
    
    def _calculate_liquidity_depth(self, liquidity: float, market_cap: float) -> float:
        """
        Calculate liquidity depth (0.0 = shallow, 1.0 = deep)
        
        Args:
            liquidity: Available liquidity
            market_cap: Market capitalization
            
        Returns:
            Depth value (0.0 to 1.0)
        """
        if market_cap == 0:
            return 0.0
        
        # Ratio of liquidity to market cap
        ratio = liquidity / market_cap
        return min(1.0, max(0.0, ratio * 10))  # Normalize
    
    def _calculate_volatility(self, curve_data: Dict[str, Any]) -> float:
        """
        Calculate price volatility
        
        Args:
            curve_data: Curve data with price history
            
        Returns:
            Volatility value (0.0 to 1.0)
        """
        # Simplified - would use price history in real implementation
        price_changes = curve_data.get("price_changes", [])
        
        if not price_changes:
            return 0.0
        
        # Calculate standard deviation of price changes
        if len(price_changes) < 2:
            return 0.0
        
        mean = sum(price_changes) / len(price_changes)
        variance = sum((x - mean) ** 2 for x in price_changes) / len(price_changes)
        std_dev = variance ** 0.5
        
        # Normalize to 0-1
        return min(1.0, std_dev / 0.1)  # Assuming 0.1 is high volatility
    
    def get_cached_analysis(self, token_mint: Pubkey) -> Optional[Dict[str, Any]]:
        """
        Get cached analysis if available
        
        Args:
            token_mint: Token mint address
            
        Returns:
            Cached analysis or None
        """
        return self.cache.get(str(token_mint))
    
    def clear_cache(self):
        """Clear analysis cache"""
        self.cache.clear()
        logger.debug("Analysis cache cleared")

