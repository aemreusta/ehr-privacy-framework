"""
Encryption module for privacy-preserving EHR data.

This module provides implementations of advanced encryption techniques:
- Homomorphic Encryption: Allows computations on encrypted data

Classes:
    HomomorphicEncryption: Implementation of homomorphic encryption using Pyfhel
"""

try:
    from .homomorphic_encryption import HomomorphicEncryption

    __all__ = ["HomomorphicEncryption"]
except ImportError:
    # Pyfhel not available
    __all__ = []
