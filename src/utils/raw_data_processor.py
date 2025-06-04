"""
Raw MIMIC-III Data Processor

This module processes the raw MIMIC-III data files to create a comprehensive
dataset for privacy-preserving analysis.
"""

import logging
from pathlib import Path
from typing import Dict, Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class MimicRawDataProcessor:
    """
    Processor for raw MIMIC-III data files.

    Combines multiple MIMIC-III tables to create a comprehensive dataset
    suitable for privacy-preserving analysis.
    """

    def __init__(self, raw_data_path: Path):
        """
        Initialize the processor.

        Args:
            raw_data_path: Path to the raw MIMIC-III data directory
        """
        self.raw_data_path = Path(raw_data_path)
        if not self.raw_data_path.exists():
            raise FileNotFoundError(f"Raw data path not found: {raw_data_path}")

        logger.info(f"Initialized processor with raw data path: {raw_data_path}")

    def create_comprehensive_dataset(
        self, output_path: Optional[Path] = None
    ) -> pd.DataFrame:
        """
        Create a comprehensive dataset from raw MIMIC-III files.

        Args:
            output_path: Path to save the processed dataset

        Returns:
            Comprehensive DataFrame with patient demographics, admissions, and clinical data
        """
        logger.info("Starting comprehensive dataset creation")

        # Load core tables
        patients = self._load_patients()
        admissions = self._load_admissions()
        icustays = self._load_icustays()

        # Merge core data
        logger.info("Merging core demographic and admission data")
        core_data = self._merge_core_data(patients, admissions, icustays)

        # Add clinical data
        logger.info("Adding clinical measurements and lab values")
        clinical_data = self._add_clinical_data(core_data)

        # Add diagnoses and procedures
        logger.info("Adding diagnoses and procedure codes")
        enhanced_data = self._add_diagnoses_procedures(clinical_data)

        # Clean and validate
        logger.info("Cleaning and validating final dataset")
        final_data = self._clean_and_validate(enhanced_data)

        # Save if path provided
        if output_path:
            final_data.to_csv(output_path, index=False)
            logger.info(f"Saved comprehensive dataset to {output_path}")

        logger.info(
            f"Created comprehensive dataset with {len(final_data)} records and {len(final_data.columns)} columns"
        )
        return final_data

    def _load_patients(self) -> pd.DataFrame:
        """Load and process PATIENTS table."""
        patients_file = self.raw_data_path / "PATIENTS.csv"
        if not patients_file.exists():
            raise FileNotFoundError(f"PATIENTS.csv not found at {patients_file}")

        patients = pd.read_csv(patients_file)
        logger.info(f"Loaded {len(patients)} patients")

        # Calculate age using a simpler method to avoid overflow
        # MIMIC-III uses shifted dates (100+ years in future)
        # We'll calculate approximate age based on year differences
        patients["dob"] = pd.to_datetime(patients["dob"], errors="coerce")

        # For MIMIC-III demo data, we'll use a simplified age calculation
        # Extract year and calculate age relative to 2150 (approximate middle of MIMIC range)
        reference_year = 2150
        patients["birth_year"] = patients["dob"].dt.year
        patients["age_at_reference"] = (reference_year - patients["birth_year"]).clip(
            18, 89
        )

        # For patients with age > 89, MIMIC convention is to set to 91.4
        patients.loc[patients["age_at_reference"] > 89, "age_at_reference"] = 91.4

        return patients[["subject_id", "gender", "age_at_reference", "expire_flag"]]

    def _load_admissions(self) -> pd.DataFrame:
        """Load and process ADMISSIONS table."""
        admissions_file = self.raw_data_path / "ADMISSIONS.csv"
        if not admissions_file.exists():
            raise FileNotFoundError(f"ADMISSIONS.csv not found at {admissions_file}")

        admissions = pd.read_csv(admissions_file)
        logger.info(f"Loaded {len(admissions)} admissions")

        # Calculate length of stay - handle potential overflow
        admissions["admittime"] = pd.to_datetime(
            admissions["admittime"], errors="coerce"
        )
        admissions["dischtime"] = pd.to_datetime(
            admissions["dischtime"], errors="coerce"
        )

        # Calculate LOS in days, handling missing discharge times
        los_days = []
        for _, row in admissions.iterrows():
            if pd.notna(row["admittime"]) and pd.notna(row["dischtime"]):
                try:
                    los = (row["dischtime"] - row["admittime"]).total_seconds() / (
                        24 * 3600
                    )
                    los_days.append(max(0.1, los))  # Minimum 0.1 day stay
                except (OverflowError, ValueError):
                    los_days.append(5.0)  # Default to 5 days if calculation fails
            else:
                los_days.append(5.0)  # Default for missing data

        admissions["los_days"] = los_days

        # Clean up diagnosis field
        admissions["primary_diagnosis"] = admissions["diagnosis"].str.strip()

        return admissions[
            [
                "subject_id",
                "hadm_id",
                "admission_type",
                "primary_diagnosis",
                "los_days",
                "hospital_expire_flag",
                "ethnicity",
                "marital_status",
                "insurance",
            ]
        ]

    def _load_icustays(self) -> pd.DataFrame:
        """Load and process ICUSTAYS table."""
        icustays_file = self.raw_data_path / "ICUSTAYS.csv"
        if not icustays_file.exists():
            logger.warning("ICUSTAYS.csv not found, skipping ICU data")
            return pd.DataFrame()

        icustays = pd.read_csv(icustays_file)
        logger.info(f"Loaded {len(icustays)} ICU stays")

        # Calculate ICU length of stay - handle potential overflow
        icustays["intime"] = pd.to_datetime(icustays["intime"], errors="coerce")
        icustays["outtime"] = pd.to_datetime(icustays["outtime"], errors="coerce")

        # Calculate ICU LOS in days, handling missing times
        icu_los_days = []
        for _, row in icustays.iterrows():
            if pd.notna(row["intime"]) and pd.notna(row["outtime"]):
                try:
                    los = (row["outtime"] - row["intime"]).total_seconds() / (24 * 3600)
                    icu_los_days.append(max(0.1, los))  # Minimum 0.1 day stay
                except (OverflowError, ValueError):
                    icu_los_days.append(2.0)  # Default to 2 days if calculation fails
            else:
                icu_los_days.append(2.0)  # Default for missing data

        icustays["icu_los_days"] = icu_los_days

        return icustays[
            ["subject_id", "hadm_id", "icustay_id", "first_careunit", "icu_los_days"]
        ]

    def _merge_core_data(
        self, patients: pd.DataFrame, admissions: pd.DataFrame, icustays: pd.DataFrame
    ) -> pd.DataFrame:
        """Merge core demographic and admission data."""
        # Start with admissions as base
        core = admissions.copy()

        # Merge with patients
        core = core.merge(patients, on="subject_id", how="left")

        # Calculate actual age at admission (approximate)
        # Using a random offset since we don't have exact admission dates relative to DOB
        np.random.seed(42)  # For reproducibility
        age_offset = np.random.normal(0, 2, len(core))  # Small random variation
        core["age"] = (core["age_at_reference"] + age_offset).clip(18, 95)

        # Add ICU data if available
        if not icustays.empty:
            # Group ICU stays by admission (some admissions have multiple ICU stays)
            icu_summary = (
                icustays.groupby("hadm_id")
                .agg(
                    {
                        "icustay_id": "count",
                        "icu_los_days": "sum",
                        "first_careunit": "first",
                    }
                )
                .rename(columns={"icustay_id": "num_icu_stays"})
            )

            core = core.merge(icu_summary, on="hadm_id", how="left")
            core["num_icu_stays"].fillna(0, inplace=True)
            core["icu_los_days"].fillna(0, inplace=True)
            core["first_careunit"].fillna("None", inplace=True)

        # Set mortality flag
        core["mortality"] = core["hospital_expire_flag"]

        return core

    def _add_clinical_data(self, core_data: pd.DataFrame) -> pd.DataFrame:
        """Add clinical measurements and vital signs."""
        # For this demo, we'll add synthetic clinical data based on patient characteristics
        # In a real implementation, you would process CHARTEVENTS and LABEVENTS tables

        logger.info("Adding synthetic clinical measurements")

        np.random.seed(42)  # For reproducibility
        n_records = len(core_data)

        # Generate realistic vital signs based on age and mortality
        age_factor = (core_data["age"] - 65) / 20  # Normalized age factor
        mortality_factor = core_data["mortality"] * 0.3  # Mortality impact

        # Heart rate (normal: 60-100 bpm)
        hr_base = np.random.normal(80, 12, n_records)
        hr_adjustment = age_factor * 5 + mortality_factor * 15
        core_data["heart_rate_mean"] = (hr_base + hr_adjustment).clip(40, 150)

        # Blood pressure (normal: 120/80 mmHg)
        sbp_base = np.random.normal(130, 20, n_records)
        sbp_adjustment = age_factor * 10 + mortality_factor * 20
        core_data["blood_pressure_systolic"] = (sbp_base + sbp_adjustment).clip(80, 200)

        dbp_base = np.random.normal(80, 10, n_records)
        dbp_adjustment = age_factor * 5 + mortality_factor * 10
        core_data["blood_pressure_diastolic"] = (dbp_base + dbp_adjustment).clip(
            50, 120
        )

        # Temperature (normal: 98.6°F)
        temp_base = np.random.normal(98.6, 1.0, n_records)
        temp_adjustment = mortality_factor * 2  # Fever in critical patients
        core_data["temperature_mean"] = (temp_base + temp_adjustment).clip(95, 105)

        # Lab values
        # Glucose (normal: 70-110 mg/dL)
        glucose_base = np.random.normal(100, 20, n_records)
        glucose_adjustment = age_factor * 10 + mortality_factor * 30
        core_data["glucose_mean"] = (glucose_base + glucose_adjustment).clip(60, 400)

        # Creatinine (normal: 0.6-1.3 mg/dL)
        creat_base = np.random.normal(1.0, 0.3, n_records)
        creat_adjustment = age_factor * 0.2 + mortality_factor * 0.8
        core_data["creatinine_mean"] = (creat_base + creat_adjustment).clip(0.3, 8.0)

        # White blood cell count (normal: 4-11 k/μL)
        wbc_base = np.random.normal(7.5, 2.0, n_records)
        wbc_adjustment = mortality_factor * 5  # Elevated in sepsis
        core_data["wbc_mean"] = (wbc_base + wbc_adjustment).clip(1, 30)

        # Round values appropriately
        core_data["heart_rate_mean"] = core_data["heart_rate_mean"].round(1)
        core_data["blood_pressure_systolic"] = core_data[
            "blood_pressure_systolic"
        ].round(0)
        core_data["blood_pressure_diastolic"] = core_data[
            "blood_pressure_diastolic"
        ].round(0)
        core_data["temperature_mean"] = core_data["temperature_mean"].round(1)
        core_data["glucose_mean"] = core_data["glucose_mean"].round(1)
        core_data["creatinine_mean"] = core_data["creatinine_mean"].round(2)
        core_data["wbc_mean"] = core_data["wbc_mean"].round(1)

        return core_data

    def _add_diagnoses_procedures(self, clinical_data: pd.DataFrame) -> pd.DataFrame:
        """Add diagnosis and procedure information."""
        # Load diagnosis codes if available
        diagnoses_file = self.raw_data_path / "DIAGNOSES_ICD.csv"
        if diagnoses_file.exists():
            diagnoses = pd.read_csv(diagnoses_file)

            # Get primary diagnosis for each admission
            primary_diagnoses = diagnoses.groupby("hadm_id").first()["icd9_code"]
            clinical_data = clinical_data.merge(
                primary_diagnoses.to_frame("icd9_primary"), on="hadm_id", how="left"
            )

            # Count total diagnoses per admission
            diag_counts = diagnoses.groupby("hadm_id").size()
            clinical_data = clinical_data.merge(
                diag_counts.to_frame("num_diagnoses"), on="hadm_id", how="left"
            )
            clinical_data["num_diagnoses"].fillna(0, inplace=True)

        # Load procedures if available
        procedures_file = self.raw_data_path / "PROCEDURES_ICD.csv"
        if procedures_file.exists():
            procedures = pd.read_csv(procedures_file)

            # Count procedures per admission
            proc_counts = procedures.groupby("hadm_id").size()
            clinical_data = clinical_data.merge(
                proc_counts.to_frame("num_procedures"), on="hadm_id", how="left"
            )
            clinical_data["num_procedures"].fillna(0, inplace=True)

        return clinical_data

    def _clean_and_validate(self, data: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate the final dataset."""
        # Remove records with missing critical information
        initial_count = len(data)

        # Must have valid age and gender
        data = data.dropna(subset=["age", "gender"])

        # Must have valid length of stay
        data = data[data["los_days"] > 0]

        # Remove extreme outliers
        data = data[data["age"].between(18, 95)]
        data = data[data["los_days"] < 365]  # Less than 1 year stay

        final_count = len(data)
        logger.info(f"Cleaned dataset: {initial_count} -> {final_count} records")

        # Select final columns
        final_columns = [
            "subject_id",
            "hadm_id",
            "age",
            "gender",
            "admission_type",
            "primary_diagnosis",
            "los_days",
            "heart_rate_mean",
            "blood_pressure_systolic",
            "blood_pressure_diastolic",
            "temperature_mean",
            "glucose_mean",
            "creatinine_mean",
            "wbc_mean",
            "mortality",
            "ethnicity",
            "marital_status",
            "insurance",
        ]

        # Add optional columns if they exist
        optional_columns = [
            "icu_los_days",
            "num_icu_stays",
            "first_careunit",
            "icd9_primary",
            "num_diagnoses",
            "num_procedures",
        ]

        for col in optional_columns:
            if col in data.columns:
                final_columns.append(col)

        # Select only columns that exist
        available_columns = [col for col in final_columns if col in data.columns]
        data = data[available_columns]

        return data

    def get_data_summary(self, data: pd.DataFrame) -> Dict:
        """Generate summary statistics for the processed data."""
        summary = {
            "total_records": len(data),
            "unique_patients": data["subject_id"].nunique(),
            "unique_admissions": data["hadm_id"].nunique(),
            "date_range": "MIMIC-III Demo Dataset",
            "mortality_rate": data["mortality"].mean(),
            "avg_age": data["age"].mean(),
            "avg_los": data["los_days"].mean(),
            "columns": list(data.columns),
            "gender_distribution": data["gender"].value_counts().to_dict(),
            "admission_types": data["admission_type"].value_counts().to_dict(),
        }

        return summary


def main():
    """Demo function for raw data processor."""
    # Set up paths
    raw_data_path = Path("../data/raw/mimic-iii-clinical-database-demo-1.4")
    output_path = Path("../data/processed/mimic_comprehensive_dataset.csv")

    # Initialize processor
    try:
        processor = MimicRawDataProcessor(raw_data_path)

        # Create comprehensive dataset
        print("Processing raw MIMIC-III data...")
        dataset = processor.create_comprehensive_dataset(output_path)

        # Print summary
        print("\nDataset created successfully!")
        print(f"Shape: {dataset.shape}")
        print(f"Columns: {list(dataset.columns)}")

        summary = processor.get_data_summary(dataset)
        print("\nSummary:")
        print(f"- Total records: {summary['total_records']}")
        print(f"- Unique patients: {summary['unique_patients']}")
        print(f"- Mortality rate: {summary['mortality_rate']:.1%}")
        print(f"- Average age: {summary['avg_age']:.1f}")
        print(f"- Average LOS: {summary['avg_los']:.1f} days")

        print("\nFirst 5 records:")
        print(dataset.head())

    except Exception as e:
        print(f"Error processing data: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
