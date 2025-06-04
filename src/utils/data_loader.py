"""
Data loading and preprocessing utilities for MIMIC-III EHR data.

This module provides functions for loading, cleaning, and preprocessing
the MIMIC-III dataset for privacy-preserving analysis.
"""

import logging
from pathlib import Path
from typing import Dict, Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class DataLoader:
    """
    Data loader class for MIMIC-III EHR data processing.

    This class provides methods for loading, cleaning, and preprocessing
    MIMIC-III data for privacy-preserving analysis.
    """

    def __init__(self, data_path: Optional[Path] = None):
        """
        Initialize DataLoader.

        Args:
            data_path: Path to the data directory
        """
        self.data_path = data_path or Path("../data")
        self.raw_path = self.data_path / "raw"
        self.processed_path = self.data_path / "processed"

    def load_mimic_subset(self, filename: str = "mimiciii_subset.csv") -> pd.DataFrame:
        """
        Load the MIMIC-III subset data.

        Args:
            filename: Name of the subset file

        Returns:
            DataFrame containing the subset data
        """
        file_path = self.processed_path / filename

        if not file_path.exists():
            raise FileNotFoundError(f"Data file not found: {file_path}")

        logger.info(f"Loading MIMIC-III subset from {file_path}")
        df = pd.read_csv(file_path)

        logger.info(f"Loaded {len(df)} records with {len(df.columns)} columns")
        return df

    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess the raw MIMIC-III data.

        Args:
            df: Raw DataFrame

        Returns:
            Preprocessed DataFrame
        """
        logger.info("Starting data preprocessing")

        # Create a copy
        processed_df = df.copy()

        # Handle missing values
        processed_df = self._handle_missing_values(processed_df)

        # Create derived features
        processed_df = self._create_derived_features(processed_df)

        # Validate data
        processed_df = self._validate_data(processed_df)

        logger.info(f"Preprocessing completed. Final shape: {processed_df.shape}")
        return processed_df

    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values in the dataset."""
        logger.info("Handling missing values")

        # For numerical columns, fill with median
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        for col in numerical_cols:
            if df[col].isnull().any():
                median_val = df[col].median()
                df[col].fillna(median_val, inplace=True)
                logger.debug(f"Filled {col} missing values with median: {median_val}")

        # For categorical columns, fill with mode or 'Unknown'
        categorical_cols = df.select_dtypes(include=["object"]).columns
        for col in categorical_cols:
            if df[col].isnull().any():
                if len(df[col].value_counts()) > 0:
                    mode_val = df[col].mode()[0]
                    df[col].fillna(mode_val, inplace=True)
                    logger.debug(f"Filled {col} missing values with mode: {mode_val}")
                else:
                    df[col].fillna("Unknown", inplace=True)
                    logger.debug(f"Filled {col} missing values with 'Unknown'")

        return df

    def _create_derived_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create derived features for analysis."""
        logger.info("Creating derived features")

        # Age groups
        if "age" in df.columns:
            df["age_group"] = pd.cut(
                df["age"],
                bins=[0, 30, 50, 70, 100],
                labels=["18-29", "30-49", "50-69", "70+"],
            )

        # BMI categories (if height and weight available)
        if "height" in df.columns and "weight" in df.columns:
            df["bmi"] = df["weight"] / (df["height"] / 100) ** 2
            df["bmi_category"] = pd.cut(
                df["bmi"],
                bins=[0, 18.5, 25, 30, 50],
                labels=["Underweight", "Normal", "Overweight", "Obese"],
            )

        # Risk categories based on vital signs
        if all(
            col in df.columns for col in ["heart_rate_mean", "blood_pressure_systolic"]
        ):
            df["cardiac_risk"] = "Low"
            df.loc[
                (df["heart_rate_mean"] > 100) | (df["blood_pressure_systolic"] > 140),
                "cardiac_risk",
            ] = "Medium"
            df.loc[
                (df["heart_rate_mean"] > 120) | (df["blood_pressure_systolic"] > 160),
                "cardiac_risk",
            ] = "High"

        # Length of stay categories
        if "los_days" in df.columns:
            df["los_category"] = pd.cut(
                df["los_days"],
                bins=[0, 1, 3, 7, 30, 365],
                labels=["<1 day", "1-3 days", "3-7 days", "1-4 weeks", ">1 month"],
            )

        return df

    def _validate_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate and clean the processed data."""
        logger.info("Validating processed data")

        # Remove obvious outliers
        if "age" in df.columns:
            df = df[(df["age"] >= 18) & (df["age"] <= 120)]

        if "heart_rate_mean" in df.columns:
            df = df[(df["heart_rate_mean"] >= 30) & (df["heart_rate_mean"] <= 200)]

        if "blood_pressure_systolic" in df.columns:
            df = df[
                (df["blood_pressure_systolic"] >= 50)
                & (df["blood_pressure_systolic"] <= 250)
            ]

        # Remove duplicate records
        initial_count = len(df)
        df = df.drop_duplicates()
        final_count = len(df)

        if initial_count != final_count:
            logger.info(f"Removed {initial_count - final_count} duplicate records")

        return df

    def get_data_summary(self, df: pd.DataFrame) -> Dict:
        """
        Get summary statistics for the dataset.

        Args:
            df: DataFrame to summarize

        Returns:
            Dictionary containing summary statistics
        """
        summary = {
            "total_records": len(df),
            "total_columns": len(df.columns),
            "numerical_columns": len(df.select_dtypes(include=[np.number]).columns),
            "categorical_columns": len(df.select_dtypes(include=["object"]).columns),
            "missing_values": df.isnull().sum().sum(),
            "data_types": df.dtypes.to_dict(),
        }

        # Add column-specific summaries
        summary["column_summaries"] = {}
        for col in df.columns:
            if df[col].dtype in [np.number]:
                summary["column_summaries"][col] = {
                    "type": "numerical",
                    "mean": df[col].mean(),
                    "std": df[col].std(),
                    "min": df[col].min(),
                    "max": df[col].max(),
                    "missing": df[col].isnull().sum(),
                }
            else:
                summary["column_summaries"][col] = {
                    "type": "categorical",
                    "unique_values": df[col].nunique(),
                    "top_value": df[col].value_counts().index[0]
                    if len(df[col].value_counts()) > 0
                    else None,
                    "missing": df[col].isnull().sum(),
                }

        return summary

    def create_synthetic_subset(
        self, n_records: int = 1000, save_path: Optional[Path] = None
    ) -> pd.DataFrame:
        """
        Create a synthetic MIMIC-III-like dataset for testing.

        Args:
            n_records: Number of records to generate
            save_path: Path to save the synthetic data

        Returns:
            Synthetic DataFrame
        """
        logger.info(f"Creating synthetic dataset with {n_records} records")

        np.random.seed(42)  # For reproducibility

        # Generate synthetic data
        data = {
            "subject_id": range(10001, 10001 + n_records),
            "hadm_id": range(100001, 100001 + n_records),
            "age": np.random.normal(65, 15, n_records).clip(18, 100),
            "gender": np.random.choice(["M", "F"], n_records),
            "admission_type": np.random.choice(
                ["EMERGENCY", "ELECTIVE", "URGENT"], n_records, p=[0.6, 0.3, 0.1]
            ),
            "diagnosis": np.random.choice(
                [
                    "Pneumonia",
                    "Heart Disease",
                    "Diabetes",
                    "Stroke",
                    "Cancer",
                    "Kidney Disease",
                ],
                n_records,
            ),
            "los_days": np.random.exponential(5, n_records).clip(0.1, 100),
            "heart_rate_mean": np.random.normal(80, 15, n_records).clip(40, 150),
            "blood_pressure_systolic": np.random.normal(130, 20, n_records).clip(
                80, 200
            ),
            "blood_pressure_diastolic": np.random.normal(80, 10, n_records).clip(
                50, 120
            ),
            "temperature_mean": np.random.normal(98.6, 1.5, n_records).clip(95, 105),
            "glucose_mean": np.random.normal(120, 30, n_records).clip(70, 300),
            "creatinine_mean": np.random.normal(1.2, 0.5, n_records).clip(0.5, 5),
            "mortality": np.random.choice([0, 1], n_records, p=[0.85, 0.15]),
        }

        df = pd.DataFrame(data)

        # Add some realistic correlations
        # Higher age increases mortality risk
        mortality_prob = 0.05 + (df["age"] - 18) / (100 - 18) * 0.3
        df["mortality"] = np.random.binomial(1, mortality_prob)

        # Adjust vital signs based on age and mortality
        age_factor = (df["age"] - 65) / 20
        df["heart_rate_mean"] += age_factor * 5
        df["blood_pressure_systolic"] += age_factor * 10

        # Round numerical values appropriately
        df["age"] = df["age"].round(1)
        df["los_days"] = df["los_days"].round(1)
        df["heart_rate_mean"] = df["heart_rate_mean"].round(1)
        df["blood_pressure_systolic"] = df["blood_pressure_systolic"].round(0)
        df["blood_pressure_diastolic"] = df["blood_pressure_diastolic"].round(0)
        df["temperature_mean"] = df["temperature_mean"].round(1)
        df["glucose_mean"] = df["glucose_mean"].round(1)
        df["creatinine_mean"] = df["creatinine_mean"].round(1)

        # Save if path provided
        if save_path:
            df.to_csv(save_path, index=False)
            logger.info(f"Saved synthetic dataset to {save_path}")

        return df


# Convenience functions
def load_mimic_subset(
    filename: str = "mimiciii_subset.csv", data_path: Optional[Path] = None
) -> pd.DataFrame:
    """
    Convenience function to load MIMIC-III subset.

    Args:
        filename: Name of the subset file
        data_path: Path to the data directory

    Returns:
        DataFrame containing the subset data
    """
    loader = DataLoader(data_path)
    return loader.load_mimic_subset(filename)


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convenience function to preprocess data.

    Args:
        df: Raw DataFrame

    Returns:
        Preprocessed DataFrame
    """
    loader = DataLoader()
    return loader.preprocess_data(df)


def main():
    """Demo function for data loader."""
    # Create synthetic data for demonstration
    loader = DataLoader()

    print("Creating synthetic MIMIC-III-like dataset...")
    synthetic_df = loader.create_synthetic_subset(n_records=100)

    print(f"Created dataset with shape: {synthetic_df.shape}")
    print(f"Columns: {list(synthetic_df.columns)}")

    print("\nFirst 5 records:")
    print(synthetic_df.head())

    print("\nData summary:")
    summary = loader.get_data_summary(synthetic_df)
    print(f"Total records: {summary['total_records']}")
    print(f"Total columns: {summary['total_columns']}")
    print(f"Missing values: {summary['missing_values']}")

    # Test preprocessing
    print("\nTesting preprocessing...")
    processed_df = loader.preprocess_data(synthetic_df)
    print(f"Processed dataset shape: {processed_df.shape}")

    if "age_group" in processed_df.columns:
        print("Age group distribution:")
        print(processed_df["age_group"].value_counts())


if __name__ == "__main__":
    main()
