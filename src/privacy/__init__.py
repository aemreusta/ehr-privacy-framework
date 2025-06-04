"""
Privacy module for advanced privacy-preserving techniques.

This module provides implementations of differential privacy
and other advanced privacy mechanisms for EHR data.
"""

from .differential_privacy import DifferentialPrivacy

__all__ = [
    "DifferentialPrivacy",
]
