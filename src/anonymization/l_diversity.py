"""
L-Diversity Implementation for Privacy-Preserving EHR Data

L-diversity extends k-anonymity by ensuring that sensitive attributes
within each equivalence class are well-represented (diverse).
"""

import logging
from typing import Any, Dict, List

import pandas as pd

logger = logging.getLogger(__name__)


class LDiversity:
    """
    Implementation of l-diversity privacy protection.

    L-diversity ensures that each equivalence class has at least l
    well-represented values for sensitive attributes.
    """

    def __init__(self, l: int = 2, k: int = 2):
        """
        Initialize l-diversity.

        Args:
            l: Minimum number of distinct sensitive values per group
            k: Minimum group size (k-anonymity requirement)
        """
        self.l = l
        self.k = k
        logger.info(f"Initialized l-diversity with l={l}, k={k}")

    def anonymize(
        self,
        df: pd.DataFrame,
        quasi_identifiers: List[str],
        sensitive_attributes: List[str],
    ) -> pd.DataFrame:
        """
        Apply l-diversity anonymization to the dataset.

        Args:
            df: Input DataFrame
            quasi_identifiers: List of QI column names
            sensitive_attributes: List of sensitive attribute names

        Returns:
            L-diverse anonymized DataFrame
        """
        logger.info(f"Applying l-diversity to {len(df)} records")

        # Start with k-anonymity groups
        groups = self._create_k_anonymous_groups(df, quasi_identifiers)

        # Filter groups to ensure l-diversity
        l_diverse_groups = []
        suppressed_count = 0

        for group_data in groups:
            if self._satisfies_l_diversity(group_data, sensitive_attributes):
                l_diverse_groups.append(group_data)
            else:
                suppressed_count += len(group_data)
                logger.debug(
                    f"Suppressed group of size {len(group_data)} - insufficient l-diversity"
                )

        if not l_diverse_groups:
            logger.warning("No groups satisfy l-diversity requirement")
            return pd.DataFrame(columns=df.columns)

        # Combine remaining groups
        result = pd.concat(l_diverse_groups, ignore_index=True)

        logger.info(
            f"L-diversity completed: {len(result)} records retained, {suppressed_count} suppressed"
        )
        return result

    def _create_k_anonymous_groups(
        self, df: pd.DataFrame, quasi_identifiers: List[str]
    ) -> List[pd.DataFrame]:
        """Create k-anonymous groups as starting point."""
        # Generalize age into ranges
        df_gen = df.copy()

        if "age" in quasi_identifiers:
            df_gen["age"] = pd.cut(
                df_gen["age"],
                bins=5,
                labels=["18-30", "31-45", "46-60", "61-75", "76+"],
            )

        # Group by quasi-identifiers
        grouped = df_gen.groupby(quasi_identifiers)

        # Keep only groups that satisfy k-anonymity
        valid_groups = []
        for name, group in grouped:
            if len(group) >= self.k:
                valid_groups.append(group)

        return valid_groups

    def _satisfies_l_diversity(
        self, group: pd.DataFrame, sensitive_attributes: List[str]
    ) -> bool:
        """
        Check if a group satisfies l-diversity requirement.

        Args:
            group: DataFrame group to check
            sensitive_attributes: List of sensitive attributes

        Returns:
            True if group satisfies l-diversity
        """
        for attr in sensitive_attributes:
            if attr in group.columns:
                unique_values = group[attr].nunique()
                if unique_values < self.l:
                    return False
        return True

    def verify_l_diversity(
        self,
        df: pd.DataFrame,
        quasi_identifiers: List[str],
        sensitive_attributes: List[str],
    ) -> Dict[str, Any]:
        """
        Verify that the dataset satisfies l-diversity.

        Returns:
            Dictionary with verification results
        """
        # Generalize for grouping (same as in anonymization)
        df_gen = df.copy()
        if "age" in quasi_identifiers:
            df_gen["age"] = pd.cut(
                df_gen["age"],
                bins=5,
                labels=["18-30", "31-45", "46-60", "61-75", "76+"],
            )

        grouped = df_gen.groupby(quasi_identifiers)

        min_diversity = float("inf")
        total_groups = 0
        valid_groups = 0

        for name, group in grouped:
            if len(group) >= self.k:  # Only consider k-anonymous groups
                total_groups += 1
                group_diversity = min(
                    group[attr].nunique()
                    for attr in sensitive_attributes
                    if attr in group.columns
                )
                min_diversity = min(min_diversity, group_diversity)

                if group_diversity >= self.l:
                    valid_groups += 1

        return {
            "satisfies_l_diversity": min_diversity >= self.l
            if min_diversity != float("inf")
            else False,
            "min_diversity": min_diversity if min_diversity != float("inf") else 0,
            "total_groups": total_groups,
            "valid_groups": valid_groups,
            "compliance_rate": valid_groups / total_groups if total_groups > 0 else 0,
        }

    def get_statistics(
        self, original_df: pd.DataFrame, anonymized_df: pd.DataFrame
    ) -> Dict[str, float]:
        """Get l-diversity statistics."""
        return {
            "data_retention_rate": len(anonymized_df) / len(original_df),
            "suppression_rate": 1 - (len(anonymized_df) / len(original_df)),
            "l_parameter": self.l,
            "k_parameter": self.k,
        }
