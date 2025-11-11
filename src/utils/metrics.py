"""
Metrics utilities

Helper functions for calculating various metrics.
"""

from typing import List


def calculate_average(values: List[float]) -> float:
    """
    Calculate average of values
    
    Args:
        values: List of numeric values
        
    Returns:
        Average value
    """
    if not values:
        return 0.0
    return sum(values) / len(values)


def calculate_standard_deviation(values: List[float]) -> float:
    """
    Calculate standard deviation
    
    Args:
        values: List of numeric values
        
    Returns:
        Standard deviation
    """
    if not values or len(values) < 2:
        return 0.0
    
    mean = calculate_average(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    return variance ** 0.5


def normalize(value: float, min_val: float, max_val: float) -> float:
    """
    Normalize value to 0-1 range
    
    Args:
        value: Value to normalize
        min_val: Minimum value
        max_val: Maximum value
        
    Returns:
        Normalized value (0.0 to 1.0)
    """
    if max_val == min_val:
        return 0.5
    
    normalized = (value - min_val) / (max_val - min_val)
    return max(0.0, min(1.0, normalized))

