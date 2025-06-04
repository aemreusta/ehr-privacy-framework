"""
k-anonymity implementation for EHR data anonymization.

k-anonymity ensures that each record in the dataset is indistinguishable from at least
k-1 other records with respect to quasi-identifiers.
"""

import logging
from typing import Any, Dict, List

import pandas as pd


class KAnonymity:
    """
    k-anonymity implementation for privacy-preserving data anonymization.

    This class implements the k-anonymity privacy model, which ensures that each
    record in the dataset cannot be distinguished from at least k-1 other records
    based on quasi-identifier attributes.

    Attributes:
        k (int): The anonymity parameter
        generalization_rules (dict): Rules for generalizing attributes
        suppression_threshold (float): Threshold for record suppression
    """

    def __init__(self, k: int = 3, suppression_threshold: float = 0.1):
        """
        Initialize k-anonymity with specified parameters.

        Args:
            k (int): The anonymity parameter (default: 3)
            suppression_threshold (float): Maximum fraction of records to suppress (default: 0.1)
        """
        self.k = k
        self.suppression_threshold = suppression_threshold
        self.generalization_rules = {}
        self.logger = logging.getLogger(__name__)

    def anonymize(
        self, data: pd.DataFrame, quasi_identifiers: List[str]
    ) -> pd.DataFrame:
        """
        Apply k-anonymity to the dataset.

        Args:
            data (pd.DataFrame): Input dataset
            quasi_identifiers (List[str]): List of quasi-identifier columns

        Returns:
            pd.DataFrame: k-anonymous dataset
        """
        self.logger.info(
            f"Applying {self.k}-anonymity to dataset with {len(data)} records"
        )

        # Create a copy of the data
        result_data = data.copy()

        # Apply generalization and suppression
        result_data = self._apply_generalization(result_data, quasi_identifiers)
        result_data = self._apply_suppression(result_data, quasi_identifiers)

        # Verify k-anonymity property
        if self._verify_k_anonymity(result_data, quasi_identifiers):
            self.logger.info(f"Successfully achieved {self.k}-anonymity")
        else:
            self.logger.warning(f"Failed to achieve {self.k}-anonymity")

        return result_data

    def _apply_generalization(
        self, data: pd.DataFrame, quasi_identifiers: List[str]
    ) -> pd.DataFrame:
        """
        Apply generalization to quasi-identifiers.

        Args:
            data (pd.DataFrame): Input dataset
            quasi_identifiers (List[str]): List of quasi-identifier columns

        Returns:
            pd.DataFrame: Generalized dataset
        """
        result = data.copy()

        for qi in quasi_identifiers:
            if qi in data.columns:
                if data[qi].dtype in ["int64", "float64"]:
                    result[qi] = self._generalize_numerical(data[qi])
                else:
                    result[qi] = self._generalize_categorical(data[qi])

        return result

    def _generalize_numerical(self, series: pd.Series) -> pd.Series:
        """
        Generalize numerical values by creating ranges.

        Args:
            series (pd.Series): Numerical series to generalize

        Returns:
            pd.Series: Generalized series with ranges
        """
        if series.name == "age":
            # Create age ranges
            def age_to_range(age):
                if pd.isna(age):
                    return "Unknown"
                if age < 30:
                    return "18-29"
                elif age < 50:
                    return "30-49"
                elif age < 70:
                    return "50-69"
                else:
                    return "70+"

            return series.apply(age_to_range)
        else:
            # Generic numerical generalization
            quartiles = series.quantile([0.25, 0.5, 0.75])

            def value_to_range(value):
                if pd.isna(value):
                    return "Unknown"
                if value <= quartiles.iloc[0]:
                    return "Low"
                elif value <= quartiles.iloc[1]:
                    return "Medium-Low"
                elif value <= quartiles.iloc[2]:
                    return "Medium-High"
                else:
                    return "High"

            return series.apply(value_to_range)

    def _generalize_categorical(self, series: pd.Series) -> pd.Series:
        """
        Generalize categorical values.

        Args:
            series (pd.Series): Categorical series to generalize

        Returns:
            pd.Series: Generalized series
        """
        # For small groups, replace with '*'
        value_counts = series.value_counts()
        small_groups = value_counts[value_counts < self.k].index

        result = series.copy()
        result = result.replace(small_groups, "*")

        return result

    def _apply_suppression(
        self, data: pd.DataFrame, quasi_identifiers: List[str]
    ) -> pd.DataFrame:
        """
        Apply record suppression to achieve k-anonymity.

        Args:
            data (pd.DataFrame): Input dataset
            quasi_identifiers (List[str]): List of quasi-identifier columns

        Returns:
            pd.DataFrame: Dataset with suppressed records
        """
        # Group by quasi-identifiers
        groups = data.groupby(quasi_identifiers)

        # Keep only groups with size >= k
        valid_groups = []
        suppressed_count = 0

        for name, group in groups:
            if len(group) >= self.k:
                valid_groups.append(group)
            else:
                suppressed_count += len(group)

        # Check suppression threshold
        suppression_rate = suppressed_count / len(data)
        if suppression_rate > self.suppression_threshold:
            self.logger.warning(
                f"Suppression rate ({suppression_rate:.2%}) exceeds threshold"
            )

        if valid_groups:
            result = pd.concat(valid_groups, ignore_index=True)
        else:
            result = pd.DataFrame(columns=data.columns)

        self.logger.info(
            f"Suppressed {suppressed_count} records ({suppression_rate:.2%})"
        )

        return result

    def _verify_k_anonymity(
        self, data: pd.DataFrame, quasi_identifiers: List[str]
    ) -> bool:
        """
        Verify that the dataset satisfies k-anonymity.

        Args:
            data (pd.DataFrame): Dataset to verify
            quasi_identifiers (List[str]): List of quasi-identifier columns

        Returns:
            bool: True if k-anonymity is satisfied
        """
        groups = data.groupby(quasi_identifiers)
        min_group_size = groups.size().min()

        return min_group_size >= self.k

    def get_statistics(
        self, original_data: pd.DataFrame, anonymized_data: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Calculate anonymization statistics.

        Args:
            original_data (pd.DataFrame): Original dataset
            anonymized_data (pd.DataFrame): Anonymized dataset

        Returns:
            Dict[str, Any]: Statistics dictionary
        """
        suppression_rate = (len(original_data) - len(anonymized_data)) / len(
            original_data
        )

        return {
            "original_records": len(original_data),
            "anonymized_records": len(anonymized_data),
            "suppression_rate": suppression_rate,
            "k_value": self.k,
            "anonymity_achieved": self._verify_k_anonymity(
                anonymized_data,
                [col for col in anonymized_data.columns if "id" not in col.lower()],
            ),
        }


def main():
    """Demo function for k-anonymity."""
    import os
    import sys

    sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

    # Create sample data
    data = pd.DataFrame(
        {
            "age": [25, 26, 27, 35, 36, 45, 46, 55, 56, 65],
            "gender": ["M", "F", "M", "F", "M", "F", "M", "F", "M", "F"],
            "zipcode": [
                "12345",
                "12346",
                "12345",
                "54321",
                "54322",
                "98765",
                "98766",
                "11111",
                "11112",
                "22222",
            ],
            "diagnosis": [
                "Flu",
                "Cold",
                "Flu",
                "Diabetes",
                "Diabetes",
                "Hypertension",
                "Hypertension",
                "Cancer",
                "Cancer",
                "Heart Disease",
            ],
        }
    )

    print("Original data:")
    print(data)
    print(f"\nDataset shape: {data.shape}")

    # Apply k-anonymity
    k_anon = KAnonymity(k=2)
    anonymized = k_anon.anonymize(data, ["age", "gender", "zipcode"])

    print(f"\n{k_anon.k}-anonymous data:")
    print(anonymized)
    print(f"\nAnonymized dataset shape: {anonymized.shape}")

    # Get statistics
    stats = k_anon.get_statistics(data, anonymized)
    print(f"\nStatistics: {stats}")


if __name__ == "__main__":
    main()
