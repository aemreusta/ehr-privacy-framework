"""
Healthcare Role-Based Access Control (RBAC) Module

This module provides comprehensive access control functionality specifically
designed for healthcare environments, with fine-grained role and permission
management compliant with HIPAA, GDPR, and other healthcare regulations.
"""

from .rbac import HealthcareRBAC

__all__ = ["HealthcareRBAC"]
