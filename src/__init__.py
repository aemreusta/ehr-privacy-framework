"""
Privacy-Preserving Electronic Health Records (EHR) Framework

This package provides implementations of various privacy-preserving techniques
for securing electronic health records while maintaining data utility.

Modules:
    anonymization: k-anonymity, l-diversity, and t-closeness implementations
    privacy: Differential privacy mechanisms
    encryption: Homomorphic encryption for computation on encrypted data
    utils: Common utilities and data processing functions
"""

__version__ = "1.0.0"
__author__ = "Privacy-Preserving EHR Team"

# Import main classes for easy access
from .anonymization import KAnonymity, LDiversity, TCloseness
from .privacy import DifferentialPrivacy
from .utils import DataLoader

# Try to import homomorphic encryption (optional dependency)
try:
    from .encryption import HomomorphicEncryption

    __all__ = [
        "KAnonymity",
        "LDiversity",
        "TCloseness",
        "DifferentialPrivacy",
        "HomomorphicEncryption",
        "DataLoader",
    ]
except ImportError:
    __all__ = [
        "KAnonymity",
        "LDiversity",
        "TCloseness",
        "DifferentialPrivacy",
        "DataLoader",
    ]
