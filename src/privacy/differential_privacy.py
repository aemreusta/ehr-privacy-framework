"""
Differential Privacy Implementation for EHR Data

Differential privacy provides mathematical guarantees that the presence
or absence of any individual in the dataset does not significantly
affect the output of statistical queries.
"""

import logging
from typing import Any, Dict, List

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class DifferentialPrivacy:
    """
    Implementation of differential privacy mechanisms for EHR data.

    Provides epsilon-differential privacy through the Laplace mechanism
    and other noise addition techniques.
    """

    def __init__(self, epsilon: float = 1.0):
        """
        Initialize differential privacy.

        Args:
            epsilon: Privacy budget (smaller = more private)
        """
        self.epsilon = epsilon
        logger.info(f"Initialized differential privacy with ε={epsilon}")

    def laplace_mechanism(self, true_value: float, sensitivity: float) -> float:
        """
        Apply Laplace mechanism for differential privacy.

        Args:
            true_value: The actual statistical value
            sensitivity: Global sensitivity of the query

        Returns:
            Noisy value with differential privacy guarantee
        """
        scale = sensitivity / self.epsilon
        noise = np.random.laplace(0, scale)
        return true_value + noise

    def private_count(self, data: pd.Series, condition: Any = None) -> float:
        """
        Compute differentially private count.

        Args:
            data: Data series to count
            condition: Optional condition for filtering

        Returns:
            Noisy count with differential privacy
        """
        if condition is not None:
            true_count = (data == condition).sum()
        else:
            true_count = len(data)

        # Sensitivity of count query is 1
        return max(0, self.laplace_mechanism(true_count, sensitivity=1.0))

    def private_mean(self, data: pd.Series, data_range: tuple = None) -> float:
        """
        Compute differentially private mean.

        Args:
            data: Numerical data series
            data_range: (min, max) range of data for sensitivity calculation

        Returns:
            Noisy mean with differential privacy
        """
        if data_range is None:
            data_range = (data.min(), data.max())

        true_mean = data.mean()
        # Sensitivity of mean is (max - min) / n
        sensitivity = (data_range[1] - data_range[0]) / len(data)

        return self.laplace_mechanism(true_mean, sensitivity)

    def private_histogram(self, data: pd.Series, bins: int = 10) -> Dict[str, float]:
        """
        Compute differentially private histogram.

        Args:
            data: Data series for histogram
            bins: Number of bins

        Returns:
            Dictionary with bin labels and noisy counts
        """
        if data.dtype in ["object", "category"]:
            # Categorical data
            true_counts = data.value_counts()
            private_counts = {}

            for category, count in true_counts.items():
                private_counts[str(category)] = max(
                    0, self.laplace_mechanism(count, sensitivity=1.0)
                )
        else:
            # Numerical data
            hist, bin_edges = np.histogram(data, bins=bins)
            private_counts = {}

            for i, count in enumerate(hist):
                bin_label = f"{bin_edges[i]:.1f}-{bin_edges[i + 1]:.1f}"
                private_counts[bin_label] = max(
                    0, self.laplace_mechanism(count, sensitivity=1.0)
                )

        return private_counts

    def private_correlation(
        self, data1: pd.Series, data2: pd.Series, data_ranges: tuple = None
    ) -> float:
        """
        Compute differentially private correlation coefficient.

        Args:
            data1: First data series
            data2: Second data series
            data_ranges: ((min1, max1), (min2, max2)) for sensitivity

        Returns:
            Noisy correlation with differential privacy
        """
        true_corr = data1.corr(data2)

        # Simplified sensitivity calculation for correlation
        # In practice, this would require more sophisticated analysis
        sensitivity = 2.0 / len(data1)  # Approximate sensitivity

        noisy_corr = self.laplace_mechanism(true_corr, sensitivity)

        # Clamp to valid correlation range [-1, 1]
        return np.clip(noisy_corr, -1, 1)

    def private_summary_statistics(
        self,
        df: pd.DataFrame,
        numerical_cols: List[str] = None,
        categorical_cols: List[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate differentially private summary statistics.

        Args:
            df: Input DataFrame
            numerical_cols: List of numerical columns to analyze
            categorical_cols: List of categorical columns to analyze

        Returns:
            Dictionary with private summary statistics
        """
        logger.info("Computing differentially private summary statistics")

        if numerical_cols is None:
            numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        if categorical_cols is None:
            categorical_cols = df.select_dtypes(
                include=["object", "category"]
            ).columns.tolist()

        summary = {
            "total_records": self.private_count(df.index),
            "numerical_statistics": {},
            "categorical_statistics": {},
        }

        # Numerical statistics
        for col in numerical_cols:
            if col in df.columns:
                col_data = df[col].dropna()
                data_range = (col_data.min(), col_data.max())

                summary["numerical_statistics"][col] = {
                    "count": self.private_count(col_data),
                    "mean": self.private_mean(col_data, data_range),
                    "min": data_range[
                        0
                    ],  # These don't need privacy (bounds are public)
                    "max": data_range[1],
                }

        # Categorical statistics
        for col in categorical_cols:
            if col in df.columns:
                col_data = df[col].dropna()
                summary["categorical_statistics"][col] = {
                    "count": self.private_count(col_data),
                    "unique_values": self.private_count(col_data.unique()),
                    "top_categories": self.private_histogram(col_data),
                }

        return summary

    def add_noise_to_dataset(
        self,
        df: pd.DataFrame,
        numerical_cols: List[str] = None,
        noise_scale: float = 0.1,
    ) -> pd.DataFrame:
        """
        Add calibrated noise to numerical columns in dataset.

        Args:
            df: Input DataFrame
            numerical_cols: Columns to add noise to
            noise_scale: Scale factor for noise

        Returns:
            DataFrame with noisy numerical values
        """
        df_noisy = df.copy()

        if numerical_cols is None:
            numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        for col in numerical_cols:
            if col in df.columns:
                # Calculate sensitivity based on data range
                data_range = df[col].max() - df[col].min()
                sensitivity = data_range * noise_scale

                # Add Laplace noise
                noise = np.random.laplace(0, sensitivity / self.epsilon, size=len(df))
                df_noisy[col] = df[col] + noise

        logger.info(
            f"Added differential privacy noise to {len(numerical_cols)} columns"
        )
        return df_noisy

    def privacy_budget_analysis(self, num_queries: int) -> Dict[str, float]:
        """
        Analyze privacy budget consumption.

        Args:
            num_queries: Number of queries executed

        Returns:
            Privacy budget analysis
        """
        epsilon_per_query = self.epsilon / num_queries

        return {
            "total_epsilon": self.epsilon,
            "num_queries": num_queries,
            "epsilon_per_query": epsilon_per_query,
            "remaining_budget": max(
                0, self.epsilon - (num_queries * epsilon_per_query)
            ),
            "privacy_level": "High"
            if self.epsilon < 1.0
            else "Medium"
            if self.epsilon < 5.0
            else "Low",
        }

    def get_utility_metrics(
        self, original_stats: Dict, private_stats: Dict
    ) -> Dict[str, float]:
        """
        Calculate utility metrics comparing original and private statistics.

        Args:
            original_stats: True statistics
            private_stats: Differentially private statistics

        Returns:
            Utility metrics
        """
        metrics = {"mean_absolute_error": 0, "relative_error": 0, "utility_score": 0}

        # Compare numerical statistics
        errors = []
        relative_errors = []

        if "numerical_statistics" in private_stats:
            for col in private_stats["numerical_statistics"]:
                if col in original_stats.get("numerical_statistics", {}):
                    orig_mean = original_stats["numerical_statistics"][col]["mean"]
                    priv_mean = private_stats["numerical_statistics"][col]["mean"]

                    abs_error = abs(orig_mean - priv_mean)
                    rel_error = abs_error / abs(orig_mean) if orig_mean != 0 else 0

                    errors.append(abs_error)
                    relative_errors.append(rel_error)

        if errors:
            metrics["mean_absolute_error"] = np.mean(errors)
            metrics["relative_error"] = np.mean(relative_errors)
            metrics["utility_score"] = 1 - min(1, np.mean(relative_errors))

        return metrics
