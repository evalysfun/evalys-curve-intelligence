"""
Configuration settings
"""

import os


class Settings:
    """Application settings"""
    
    # Solana RPC
    SOLANA_RPC_URL: str = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
    
    # Analysis settings
    DEFAULT_TIME_WINDOW_MINUTES: int = int(os.getenv("DEFAULT_TIME_WINDOW_MINUTES", "30"))
    SNIPER_DETECTION_WINDOW: int = int(os.getenv("SNIPER_DETECTION_WINDOW", "5"))
    
    # Risk thresholds
    HIGH_RISK_THRESHOLD: float = float(os.getenv("HIGH_RISK_THRESHOLD", "0.7"))
    CRITICAL_RISK_THRESHOLD: float = float(os.getenv("CRITICAL_RISK_THRESHOLD", "0.9"))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # API settings
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8003"))
    API_DEBUG: bool = os.getenv("API_DEBUG", "false").lower() == "true"

