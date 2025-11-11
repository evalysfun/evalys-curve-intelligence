"""
Risk Detector

Detects risks in bonding curves: snipers, buy clusters, liquidity risks.
"""

from enum import Enum
from typing import Dict, Any, List, Optional
from solders.pubkey import Pubkey
from datetime import datetime, timedelta
from ..data.collectors import DataCollector
from ..utils.logger import get_logger

logger = get_logger(__name__)


class RiskLevel(str, Enum):
    """Risk level enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskDetector:
    """
    Detects risks in bonding curves
    """
    
    def __init__(self, data_collector: Optional[DataCollector] = None):
        """
        Initialize risk detector
        
        Args:
            data_collector: Data collector instance
        """
        self.data_collector = data_collector
        self.transaction_history: Dict[str, List[Dict[str, Any]]] = {}
        logger.info("RiskDetector initialized")
    
    async def detect_sniper_window(
        self,
        token_mint: Pubkey,
        time_window_minutes: int = 5
    ) -> Dict[str, Any]:
        """
        Detect if snipers are active
        
        Args:
            token_mint: Token mint address
            time_window_minutes: Time window to analyze
            
        Returns:
            Dictionary with sniper detection results
        """
        if self.data_collector:
            transactions = await self.data_collector.get_recent_transactions(
                token_mint,
                time_window_minutes
            )
        else:
            transactions = self.transaction_history.get(str(token_mint), [])
        
        # Analyze transaction patterns
        sniper_indicators = self._analyze_sniper_patterns(transactions, time_window_minutes)
        
        is_active = sniper_indicators["probability"] > 0.6
        risk_level = self._calculate_sniper_risk(sniper_indicators["probability"])
        
        result = {
            "token_mint": str(token_mint),
            "is_active": is_active,
            "risk_level": risk_level.value,
            "probability": sniper_indicators["probability"],
            "indicators": sniper_indicators,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.debug(
            f"Sniper detection for {token_mint}: active={is_active}, "
            f"risk={risk_level.value}, prob={sniper_indicators['probability']:.2f}"
        )
        
        return result
    
    async def detect_buy_clusters(
        self,
        token_mint: Pubkey,
        time_window_minutes: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Detect buy clusters (grouped transactions)
        
        Args:
            token_mint: Token mint address
            time_window_minutes: Time window to analyze
            
        Returns:
            List of detected clusters
        """
        if self.data_collector:
            transactions = await self.data_collector.get_recent_transactions(
                token_mint,
                time_window_minutes
            )
        else:
            transactions = self.transaction_history.get(str(token_mint), [])
        
        # Group transactions by time
        clusters = self._identify_clusters(transactions, time_window_minutes)
        
        logger.debug(f"Detected {len(clusters)} buy clusters for {token_mint}")
        
        return clusters
    
    async def assess_risk(
        self,
        token_mint: Pubkey,
        curve_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Comprehensive risk assessment
        
        Args:
            token_mint: Token mint address
            curve_data: Optional curve data
            
        Returns:
            Dictionary with risk assessment
        """
        # Detect sniper activity
        sniper_result = await self.detect_sniper_window(token_mint)
        
        # Detect buy clusters
        clusters = await self.detect_buy_clusters(token_mint)
        
        # Assess liquidity risk
        liquidity_risk = self._assess_liquidity_risk(curve_data)
        
        # Calculate overall risk
        overall_risk = self._calculate_overall_risk(
            sniper_result,
            clusters,
            liquidity_risk
        )
        
        assessment = {
            "token_mint": str(token_mint),
            "overall_risk": overall_risk.value,
            "sniper_activity": sniper_result,
            "buy_clusters": clusters,
            "liquidity_risk": liquidity_risk,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Risk assessment for {token_mint}: {overall_risk.value}")
        
        return assessment
    
    def _analyze_sniper_patterns(
        self,
        transactions: List[Dict[str, Any]],
        time_window: int
    ) -> Dict[str, Any]:
        """
        Analyze transaction patterns for sniper activity
        
        Args:
            transactions: List of transactions
            time_window: Time window in minutes
            
        Returns:
            Dictionary with sniper indicators
        """
        if not transactions:
            return {
                "probability": 0.0,
                "transaction_count": 0,
                "avg_time_between": 0.0,
                "pattern_match": False
            }
        
        # Calculate indicators
        transaction_count = len(transactions)
        time_span = time_window * 60  # Convert to seconds
        
        # High transaction frequency suggests snipers
        frequency = transaction_count / time_span if time_span > 0 else 0
        
        # Calculate average time between transactions
        if len(transactions) > 1:
            times = [t.get("timestamp", 0) for t in transactions]
            times.sort()
            intervals = [times[i+1] - times[i] for i in range(len(times)-1)]
            avg_interval = sum(intervals) / len(intervals) if intervals else 0
        else:
            avg_interval = 0
        
        # Pattern matching (simplified)
        # Real implementation would use ML or more sophisticated pattern matching
        pattern_match = frequency > 0.1 and avg_interval < 10  # High frequency, low interval
        
        # Calculate probability (0.0 to 1.0)
        probability = min(1.0, frequency * 10)  # Normalize
        
        return {
            "probability": probability,
            "transaction_count": transaction_count,
            "frequency": frequency,
            "avg_time_between": avg_interval,
            "pattern_match": pattern_match
        }
    
    def _identify_clusters(
        self,
        transactions: List[Dict[str, Any]],
        time_window: int
    ) -> List[Dict[str, Any]]:
        """
        Identify transaction clusters
        
        Args:
            transactions: List of transactions
            time_window: Time window in minutes
            
        Returns:
            List of clusters
        """
        if not transactions:
            return []
        
        # Group transactions by time windows
        clusters = []
        cluster_window_seconds = 60  # 1 minute clusters
        
        # Sort by timestamp
        sorted_txs = sorted(transactions, key=lambda t: t.get("timestamp", 0))
        
        current_cluster = []
        cluster_start = None
        
        for tx in sorted_txs:
            tx_time = tx.get("timestamp", 0)
            
            if cluster_start is None:
                cluster_start = tx_time
                current_cluster = [tx]
            elif tx_time - cluster_start <= cluster_window_seconds:
                current_cluster.append(tx)
            else:
                # Save cluster
                if len(current_cluster) >= 2:  # At least 2 transactions
                    clusters.append({
                        "start_time": cluster_start,
                        "end_time": current_cluster[-1].get("timestamp", 0),
                        "transaction_count": len(current_cluster),
                        "total_volume": sum(t.get("amount", 0) for t in current_cluster)
                    })
                
                # Start new cluster
                cluster_start = tx_time
                current_cluster = [tx]
        
        # Save last cluster
        if len(current_cluster) >= 2:
            clusters.append({
                "start_time": cluster_start,
                "end_time": current_cluster[-1].get("timestamp", 0),
                "transaction_count": len(current_cluster),
                "total_volume": sum(t.get("amount", 0) for t in current_cluster)
            })
        
        return clusters
    
    def _assess_liquidity_risk(self, curve_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Assess liquidity risk
        
        Args:
            curve_data: Curve data
            
        Returns:
            Liquidity risk assessment
        """
        if not curve_data:
            return {
                "risk_level": RiskLevel.MEDIUM.value,
                "liquidity": 0.0,
                "risk_score": 0.5
            }
        
        liquidity = curve_data.get("liquidity", 0.0)
        market_cap = curve_data.get("market_cap", 0.0)
        
        # Calculate liquidity ratio
        if market_cap > 0:
            ratio = liquidity / market_cap
        else:
            ratio = 0.0
        
        # Assess risk
        if ratio < 0.1:
            risk_level = RiskLevel.CRITICAL
            risk_score = 0.9
        elif ratio < 0.3:
            risk_level = RiskLevel.HIGH
            risk_score = 0.7
        elif ratio < 0.5:
            risk_level = RiskLevel.MEDIUM
            risk_score = 0.5
        else:
            risk_level = RiskLevel.LOW
            risk_score = 0.3
        
        return {
            "risk_level": risk_level.value,
            "liquidity": liquidity,
            "liquidity_ratio": ratio,
            "risk_score": risk_score
        }
    
    def _calculate_overall_risk(
        self,
        sniper_result: Dict[str, Any],
        clusters: List[Dict[str, Any]],
        liquidity_risk: Dict[str, Any]
    ) -> RiskLevel:
        """
        Calculate overall risk level
        
        Args:
            sniper_result: Sniper detection result
            clusters: Buy clusters
            liquidity_risk: Liquidity risk assessment
            
        Returns:
            Overall risk level
        """
        # Weighted risk calculation
        sniper_risk = sniper_result.get("probability", 0.0)
        cluster_risk = min(1.0, len(clusters) * 0.2)  # More clusters = higher risk
        liquidity_risk_score = liquidity_risk.get("risk_score", 0.5)
        
        # Weighted average
        overall_score = (
            sniper_risk * 0.4 +
            cluster_risk * 0.3 +
            liquidity_risk_score * 0.3
        )
        
        # Determine risk level
        if overall_score >= 0.8:
            return RiskLevel.CRITICAL
        elif overall_score >= 0.6:
            return RiskLevel.HIGH
        elif overall_score >= 0.4:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW

