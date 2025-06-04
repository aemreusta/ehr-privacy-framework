"""
T-Closeness Implementation for Privacy-Preserving EHR Data

T-closeness extends l-diversity by ensuring that the distribution of
sensitive attributes within each equivalence class is close to the
overall distribution in the dataset.
"""

import logging
from typing import Any, Dict, List

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class TCloseness:
    """
    Implementation of t-closeness privacy protection.

    T-closeness ensures that the distribution of sensitive attributes
    in each equivalence class is close to the overall distribution.
    """

    def __init__(self, t: float = 0.2, k: int = 2):
        """
        Initialize t-closeness.

        Args:
            t: Maximum allowed distance between distributions (0 < t <= 1)
            k: Minimum group size (k-anonymity requirement)
        """
        self.t = t
        self.k = k
        logger.info(f"Initialized t-closeness with t={t}, k={k}")

    def anonymize(
        self,
        df: pd.DataFrame,
        quasi_identifiers: List[str],
        sensitive_attributes: List[str],
    ) -> pd.DataFrame:
        """
        Apply t-closeness anonymization to the dataset.

        Args:
            df: Input DataFrame
            quasi_identifiers: List of QI column names
            sensitive_attributes: List of sensitive attribute names

        Returns:
            T-close anonymized DataFrame
        """
        logger.info(f"Applying t-closeness to {len(df)} records")

        # Calculate global distributions for sensitive attributes
        global_distributions = self._calculate_global_distributions(
            df, sensitive_attributes
        )

        # Start with k-anonymity groups
        groups = self._create_k_anonymous_groups(df, quasi_identifiers)

        # Filter groups to ensure t-closeness
        t_close_groups = []
        suppressed_count = 0

        for group_data in groups:
            if self._satisfies_t_closeness(
                group_data, sensitive_attributes, global_distributions
            ):
                t_close_groups.append(group_data)
            else:
                suppressed_count += len(group_data)
                logger.debug(
                    f"Suppressed group of size {len(group_data)} - insufficient t-closeness"
                )

        if not t_close_groups:
            logger.warning("No groups satisfy t-closeness requirement")
            return pd.DataFrame(columns=df.columns)

        # Combine remaining groups
        result = pd.concat(t_close_groups, ignore_index=True)

        logger.info(
            f"T-closeness completed: {len(result)} records retained, {suppressed_count} suppressed"
        )
        return result

    def _create_k_anonymous_groups(
        self, df: pd.DataFrame, quasi_identifiers: List[str]
    ) -> List[pd.DataFrame]:
        """Create k-anonymous groups as starting point."""
        # Generalize age into ranges
        df_gen = df.copy()

        if "age" in quasi_identifiers:
            # Check if age is already generalized (string ranges) or still numeric
            if df_gen["age"].dtype == "object" or pd.api.types.is_string_dtype(
                df_gen["age"]
            ):
                # Age is already generalized, no need to apply pd.cut again
                logger.debug("Age column is already generalized, skipping pd.cut()")
            else:
                # Age is still numeric, apply generalization
                logger.debug("Age column is numeric, applying pd.cut()")
                # Ensure age is numeric before cutting
                df_gen["age"] = pd.to_numeric(df_gen["age"], errors="coerce")
                df_gen["age"] = pd.cut(
                    df_gen["age"],
                    bins=5,
                    labels=["18-30", "31-45", "46-60", "61-75", "76+"],
                )

        # Group by quasi-identifiers
        grouped = df_gen.groupby(quasi_identifiers)

        # Keep only groups that satisfy k-anonymity
        valid_groups = []
        for _name, group in grouped:
            if len(group) >= self.k:
                valid_groups.append(group)

        return valid_groups

    def _calculate_global_distributions(
        self, df: pd.DataFrame, sensitive_attributes: List[str]
    ) -> Dict[str, Dict[str, float]]:
        """Calculate global distributions for sensitive attributes."""
        global_distributions = {}

        for attr in sensitive_attributes:
            if attr in df.columns:
                if df[attr].dtype in ["object", "category"]:
                    # Categorical attribute
                    value_counts = df[attr].value_counts(normalize=True)
                    global_distributions[attr] = value_counts.to_dict()
                else:
                    # Numerical attribute - create histogram
                    hist, bin_edges = np.histogram(df[attr].dropna(), bins=10)
                    hist_normalized = hist / hist.sum()

                    # Create distribution dict with bin centers as keys
                    distribution = {}
                    for i in range(len(hist_normalized)):
                        distribution[f"bin_{i}"] = hist_normalized[i]

                    global_distributions[attr] = distribution

        return global_distributions

    def _satisfies_t_closeness(
        self,
        group: pd.DataFrame,
        sensitive_attributes: List[str],
        global_distributions: Dict[str, Dict[str, float]],
    ) -> bool:
        """
        Check if a group satisfies t-closeness requirement.

        Args:
            group: DataFrame group to check
            sensitive_attributes: List of sensitive attributes
            global_distributions: Global distributions for comparison

        Returns:
            True if group satisfies t-closeness
        """
        for attr in sensitive_attributes:
            if attr in group.columns and attr in global_distributions:
                group_distribution = self._calculate_group_distribution(group, attr)
                global_distribution = global_distributions[attr]

                distance = self._calculate_distribution_distance(
                    group_distribution, global_distribution
                )

                if distance > self.t:
                    return False

        return True

    def _calculate_group_distribution(
        self, group: pd.DataFrame, attribute: str
    ) -> Dict[str, float]:
        """Calculate distribution of an attribute within a group."""
        if group[attribute].dtype in ["object", "category"]:
            # Categorical attribute
            value_counts = group[attribute].value_counts(normalize=True)
            return value_counts.to_dict()
        else:
            # Numerical attribute - create histogram matching global bins
            hist, bin_edges = np.histogram(group[attribute].dropna(), bins=10)
            hist_normalized = hist / hist.sum() if hist.sum() > 0 else hist

            distribution = {}
            for i in range(len(hist_normalized)):
                distribution[f"bin_{i}"] = hist_normalized[i]

            return distribution

    def _calculate_distribution_distance(
        self, dist1: Dict[str, float], dist2: Dict[str, float]
    ) -> float:
        """
        Calculate distance between two distributions.

        Uses Earth Mover's Distance (Wasserstein distance) for categorical data.
        """
        # Get all unique values from both distributions
        all_values = set(dist1.keys()) | set(dist2.keys())

        # Convert to aligned arrays
        values1 = [dist1.get(val, 0.0) for val in sorted(all_values)]
        values2 = [dist2.get(val, 0.0) for val in sorted(all_values)]

        # For categorical data, use normalized Manhattan distance
        # This is a simplified version of Earth Mover's Distance
        distance = sum(abs(v1 - v2) for v1, v2 in zip(values1, values2)) / 2

        return distance

    def verify_t_closeness(
        self,
        df: pd.DataFrame,
        quasi_identifiers: List[str],
        sensitive_attributes: List[str],
    ) -> Dict[str, Any]:
        """
        Verify that the dataset satisfies t-closeness.

        Returns:
            Dictionary with verification results
        """
        # Calculate global distributions
        global_distributions = self._calculate_global_distributions(
            df, sensitive_attributes
        )

        # Generalize for grouping (same as in anonymization)
        df_gen = df.copy()
        if "age" in quasi_identifiers:
            # Check if age is already generalized (string ranges) or still numeric
            if df_gen["age"].dtype == "object" or pd.api.types.is_string_dtype(
                df_gen["age"]
            ):
                # Age is already generalized, no need to apply pd.cut again
                logger.debug("Age column is already generalized, skipping pd.cut()")
            else:
                # Age is still numeric, apply generalization
                logger.debug("Age column is numeric, applying pd.cut()")
                # Ensure age is numeric before cutting
                df_gen["age"] = pd.to_numeric(df_gen["age"], errors="coerce")
                df_gen["age"] = pd.cut(
                    df_gen["age"],
                    bins=5,
                    labels=["18-30", "31-45", "46-60", "61-75", "76+"],
                )

        grouped = df_gen.groupby(quasi_identifiers)

        max_distance = 0.0
        total_groups = 0
        valid_groups = 0
        distance_violations = []

        for _name, group in grouped:
            if len(group) >= self.k:  # Only consider k-anonymous groups
                total_groups += 1

                group_satisfies_t_closeness = True
                group_max_distance = 0.0

                for attr in sensitive_attributes:
                    if attr in group.columns and attr in global_distributions:
                        group_distribution = self._calculate_group_distribution(
                            group, attr
                        )
                        global_distribution = global_distributions[attr]

                        distance = self._calculate_distribution_distance(
                            group_distribution, global_distribution
                        )

                        group_max_distance = max(group_max_distance, distance)
                        max_distance = max(max_distance, distance)

                        if distance > self.t:
                            group_satisfies_t_closeness = False
                            distance_violations.append(
                                {
                                    "group": str(_name),
                                    "attribute": attr,
                                    "distance": distance,
                                    "threshold": self.t,
                                }
                            )

                if group_satisfies_t_closeness:
                    valid_groups += 1

        return {
            "satisfies_t_closeness": max_distance <= self.t,
            "max_distance": max_distance,
            "t_threshold": self.t,
            "total_groups": total_groups,
            "valid_groups": valid_groups,
            "compliance_rate": valid_groups / total_groups if total_groups > 0 else 0,
            "distance_violations": distance_violations,
        }

    def get_statistics(
        self, original_df: pd.DataFrame, anonymized_df: pd.DataFrame
    ) -> Dict[str, float]:
        """Get t-closeness statistics."""
        return {
            "data_retention_rate": len(anonymized_df) / len(original_df),
            "suppression_rate": 1 - (len(anonymized_df) / len(original_df)),
            "t_parameter": self.t,
            "k_parameter": self.k,
        }

    def analyze_distribution_distances(
        self,
        df: pd.DataFrame,
        quasi_identifiers: List[str],
        sensitive_attributes: List[str],
    ) -> Dict[str, Any]:
        """
        Analyze distribution distances across all groups.

        Returns detailed analysis of how close group distributions
        are to global distributions.
        """
        global_distributions = self._calculate_global_distributions(
            df, sensitive_attributes
        )

        # Generalize for grouping
        df_gen = df.copy()
        if "age" in quasi_identifiers:
            # Check if age is already generalized (string ranges) or still numeric
            if df_gen["age"].dtype == "object" or pd.api.types.is_string_dtype(
                df_gen["age"]
            ):
                # Age is already generalized, no need to apply pd.cut again
                logger.debug("Age column is already generalized, skipping pd.cut()")
            else:
                # Age is still numeric, apply generalization
                logger.debug("Age column is numeric, applying pd.cut()")
                # Ensure age is numeric before cutting
                df_gen["age"] = pd.to_numeric(df_gen["age"], errors="coerce")
                df_gen["age"] = pd.cut(
                    df_gen["age"],
                    bins=5,
                    labels=["18-30", "31-45", "46-60", "61-75", "76+"],
                )

        grouped = df_gen.groupby(quasi_identifiers)

        analysis = {
            "attribute_distances": {},
            "group_analysis": [],
            "summary_statistics": {},
        }

        all_distances = []

        for _name, group in grouped:
            if len(group) >= self.k:
                group_info = {
                    "group_id": str(_name),
                    "group_size": len(group),
                    "distances": {},
                    "satisfies_t_closeness": True,
                }

                for attr in sensitive_attributes:
                    if attr in group.columns and attr in global_distributions:
                        group_distribution = self._calculate_group_distribution(
                            group, attr
                        )
                        global_distribution = global_distributions[attr]

                        distance = self._calculate_distribution_distance(
                            group_distribution, global_distribution
                        )

                        group_info["distances"][attr] = distance
                        all_distances.append(distance)

                        if attr not in analysis["attribute_distances"]:
                            analysis["attribute_distances"][attr] = []
                        analysis["attribute_distances"][attr].append(distance)

                        if distance > self.t:
                            group_info["satisfies_t_closeness"] = False

                analysis["group_analysis"].append(group_info)

        # Summary statistics
        if all_distances:
            analysis["summary_statistics"] = {
                "mean_distance": np.mean(all_distances),
                "median_distance": np.median(all_distances),
                "max_distance": np.max(all_distances),
                "min_distance": np.min(all_distances),
                "std_distance": np.std(all_distances),
                "violations_count": sum(1 for d in all_distances if d > self.t),
                "violation_rate": sum(1 for d in all_distances if d > self.t)
                / len(all_distances),
            }

        return analysis
