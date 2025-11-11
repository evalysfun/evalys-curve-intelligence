"""
Pattern Recognition

Detects patterns in trading behavior: whales, bots, anomalies.
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from solders.pubkey import Pubkey
from datetime import datetime
from ..data.collectors import DataCollector
from ..utils.logger import get_logger

logger = get_logger(__name__)


class PatternType(str, Enum):
    """Pattern type enumeration"""
    WHALE_MOVEMENT = "whale_movement"
    BOT_ACTIVITY = "bot_activity"
    PUMP_PATTERN = "pump_pattern"
    DUMP_PATTERN = "dump_pattern"
    ANOMALY = "anomaly"


class PatternRecognizer:
    """
    Recognizes patterns in trading behavior
    """
    
    def __init__(self, data_collector: Optional[DataCollector] = None):
        """
        Initialize pattern recognizer
        
        Args:
            data_collector: Data collector instance
        """
        self.data_collector = data_collector
        logger.info("PatternRecognizer initialized")
    
    async def detect_patterns(
        self,
        token_mint: Pubkey,
        time_window_minutes: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Detect patterns in trading behavior
        
        Args:
            token_mint: Token mint address
            time_window_minutes: Time window to analyze
            
        Returns:
            List of detected patterns
        """
        if self.data_collector:
            transactions = await self.data_collector.get_recent_transactions(
                token_mint,
                time_window_minutes
            )
        else:
            transactions = []
        
        patterns = []
        
        # Detect whale movements
        whale_patterns = self._detect_whale_movements(transactions)
        patterns.extend(whale_patterns)
        
        # Detect bot activity
        bot_patterns = self._detect_bot_activity(transactions)
        patterns.extend(bot_patterns)
        
        # Detect pump/dump patterns
        pump_patterns = self._detect_pump_patterns(transactions)
        patterns.extend(pump_patterns)
        
        dump_patterns = self._detect_dump_patterns(transactions)
        patterns.extend(dump_patterns)
        
        # Detect anomalies
        anomalies = self._detect_anomalies(transactions)
        patterns.extend(anomalies)
        
        logger.debug(f"Detected {len(patterns)} patterns for {token_mint}")
        
        return patterns
    
    def _detect_whale_movements(
        self,
        transactions: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Detect whale (large) movements
        
        Args:
            transactions: List of transactions
            
        Returns:
            List of whale movement patterns
        """
        patterns = []
        
        if not transactions:
            return patterns
        
        # Calculate average transaction size
        amounts = [t.get("amount", 0) for t in transactions if t.get("amount", 0) > 0]
        if not amounts:
            return patterns
        
        avg_amount = sum(amounts) / len(amounts)
        threshold = avg_amount * 5  # 5x average = whale
        
        # Find whale transactions
        for tx in transactions:
            amount = tx.get("amount", 0)
            if amount >= threshold:
                patterns.append({
                    "type": PatternType.WHALE_MOVEMENT.value,
                    "timestamp": tx.get("timestamp", 0),
                    "amount": amount,
                    "wallet": tx.get("wallet", "unknown"),
                    "confidence": min(1.0, amount / (threshold * 2))
                })
        
        return patterns
    
    def _detect_bot_activity(
        self,
        transactions: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Detect bot activity patterns
        
        Args:
            transactions: List of transactions
            
        Returns:
            List of bot activity patterns
        """
        patterns = []
        
        if len(transactions) < 3:
            return patterns
        
        # Analyze timing patterns
        times = sorted([t.get("timestamp", 0) for t in transactions])
        intervals = [times[i+1] - times[i] for i in range(len(times)-1)]
        
        # Very regular intervals suggest bots
        if intervals:
            avg_interval = sum(intervals) / len(intervals)
            variance = sum((x - avg_interval) ** 2 for x in intervals) / len(intervals)
            
            # Low variance = regular pattern = likely bot
            if variance < avg_interval * 0.1 and avg_interval < 60:  # Regular, frequent
                patterns.append({
                    "type": PatternType.BOT_ACTIVITY.value,
                    "confidence": 0.8,
                    "avg_interval": avg_interval,
                    "variance": variance,
                    "transaction_count": len(transactions)
                })
        
        return patterns
    
    def _detect_pump_patterns(
        self,
        transactions: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Detect pump patterns (rapid price increase)
        
        Args:
            transactions: List of transactions
            
        Returns:
            List of pump patterns
        """
        patterns = []
        
        if len(transactions) < 5:
            return patterns
        
        # Analyze price movements
        prices = [t.get("price", 0) for t in transactions if t.get("price", 0) > 0]
        
        if len(prices) < 3:
            return patterns
        
        # Check for rapid increase
        price_changes = [(prices[i+1] - prices[i]) / prices[i] for i in range(len(prices)-1)]
        avg_change = sum(price_changes) / len(price_changes)
        
        # Rapid positive changes = pump
        if avg_change > 0.1:  # 10% average increase
            patterns.append({
                "type": PatternType.PUMP_PATTERN.value,
                "confidence": min(1.0, avg_change * 5),
                "avg_price_change": avg_change,
                "transaction_count": len(transactions)
            })
        
        return patterns
    
    def _detect_dump_patterns(
        self,
        transactions: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Detect dump patterns (rapid price decrease)
        
        Args:
            transactions: List of transactions
            
        Returns:
            List of dump patterns
        """
        patterns = []
        
        if len(transactions) < 5:
            return patterns
        
        # Analyze price movements
        prices = [t.get("price", 0) for t in transactions if t.get("price", 0) > 0]
        
        if len(prices) < 3:
            return patterns
        
        # Check for rapid decrease
        price_changes = [(prices[i+1] - prices[i]) / prices[i] for i in range(len(prices)-1)]
        avg_change = sum(price_changes) / len(price_changes)
        
        # Rapid negative changes = dump
        if avg_change < -0.1:  # 10% average decrease
            patterns.append({
                "type": PatternType.DUMP_PATTERN.value,
                "confidence": min(1.0, abs(avg_change) * 5),
                "avg_price_change": avg_change,
                "transaction_count": len(transactions)
            })
        
        return patterns
    
    def _detect_anomalies(
        self,
        transactions: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Detect anomalies in transaction patterns
        
        Args:
            transactions: List of transactions
            
        Returns:
            List of anomalies
        """
        patterns = []
        
        if not transactions:
            return patterns
        
        # Detect unusual transaction sizes
        amounts = [t.get("amount", 0) for t in transactions]
        if amounts:
            avg_amount = sum(amounts) / len(amounts)
            std_dev = (sum((x - avg_amount) ** 2 for x in amounts) / len(amounts)) ** 0.5
            
            # Transactions far from mean = anomaly
            for tx in transactions:
                amount = tx.get("amount", 0)
                if std_dev > 0 and abs(amount - avg_amount) > std_dev * 3:
                    patterns.append({
                        "type": PatternType.ANOMALY.value,
                        "timestamp": tx.get("timestamp", 0),
                        "amount": amount,
                        "deviation": abs(amount - avg_amount) / std_dev,
                        "confidence": 0.7
                    })
        
        return patterns

