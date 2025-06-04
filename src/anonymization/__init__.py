"""
Anonymization module for privacy-preserving EHR data.

This module provides implementations of various anonymization techniques:
- k-anonymity: Ensures each record is indistinguishable from at least k-1 others
- l-diversity: Ensures diversity of sensitive attributes within equivalence classes
- t-closeness: Ensures attribute distributions are close to the overall distribution

Classes:
    KAnonymity: Implementation of k-anonymity algorithm
    LDiversity: Implementation of l-diversity algorithm
    TCloseness: Implementation of t-closeness algorithm
"""

from .k_anonymity import KAnonymity
from .l_diversity import LDiversity
from .t_closeness import TCloseness

__all__ = [
    "KAnonymity",
    "LDiversity",
    "TCloseness",
]
