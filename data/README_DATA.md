# Data Directory

This directory contains the datasets used for the privacy-preserving EHR project.

## Directory Structure

```
data/
├── README_DATA.md              # This file
├── raw/                        # Original MIMIC-III files (gitignored)
├── processed/
│   └── mimiciii_subset.csv     # Small, preprocessed subset for development
└── example_output/             # Example anonymized data and results
```

## MIMIC-III Dataset

### About MIMIC-III

The Medical Information Mart for Intensive Care III (MIMIC-III) is a large, freely-available database comprising de-identified health-related data associated with over 40,000 patients who stayed in critical care units of the Beth Israel Deaconess Medical Center between 2001 and 2012.

### Key Features

- **Patients**: 46,520 patients
- **Admissions**: 58,976 hospital admissions
- **ICU Stays**: 61,532 ICU stays
- **Data Types**: Demographics, vital signs, laboratory tests, medications, caregiver notes, imaging reports, and mortality

### How to Obtain MIMIC-III

1. **Complete Required Training**
   - Complete the CITI "Data or Specimens Only Research" course
   - Upload your certificate to PhysioNet

2. **Create PhysioNet Account**
   - Visit: <https://physionet.org/>
   - Create an account with your institutional email
   - Complete the credentialing process

3. **Sign Data Use Agreement**
   - Navigate to the MIMIC-III Clinical Database page
   - Read and sign the Data Use Agreement (DUA)
   - Wait for approval (typically 1-2 business days)

4. **Download the Dataset**
   - Once approved, download the CSV files
   - Place them in the `data/raw/` directory
   - The complete dataset is approximately 6GB compressed

### Key Files in MIMIC-III

- `PATIENTS.csv` - Patient demographics and hospital expire flag
- `ADMISSIONS.csv` - Hospital admission and discharge information
- `ICUSTAYS.csv` - ICU admission and discharge information
- `CHARTEVENTS.csv` - Charted vital signs and other measurements
- `LABEVENTS.csv` - Laboratory test results
- `PRESCRIPTIONS.csv` - Medication prescriptions
- `NOTEEVENTS.csv` - Clinical notes
- `DIAGNOSES_ICD.csv` - Hospital assigned diagnoses
- `PROCEDURES_ICD.csv` - Hospital assigned procedures

## Processed Data

### mimiciii_subset.csv

For development and demonstration purposes, we provide a small subset of the MIMIC-III data that includes:

- **Size**: ~1,000 patients
- **Features**:
  - Patient demographics (age, gender)
  - Admission information
  - Selected vital signs
  - Basic laboratory values
  - Simplified diagnostic codes

### Data Schema

The processed subset contains the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `subject_id` | int | Unique patient identifier |
| `hadm_id` | int | Hospital admission identifier |
| `age` | float | Patient age at admission |
| `gender` | str | Patient gender (M/F) |
| `admission_type` | str | Type of admission |
| `diagnosis` | str | Primary diagnosis |
| `los_days` | float | Length of stay in days |
| `heart_rate_mean` | float | Mean heart rate during stay |
| `blood_pressure_systolic` | float | Systolic blood pressure |
| `blood_pressure_diastolic` | float | Diastolic blood pressure |
| `temperature_mean` | float | Mean temperature |
| `glucose_mean` | float | Mean glucose level |
| `creatinine_mean` | float | Mean creatinine level |
| `mortality` | int | Hospital mortality (0/1) |

## Example Output

The `example_output/` directory contains examples of:

- Anonymized datasets using k-anonymity, l-diversity, and t-closeness
- Encrypted data samples
- Differential privacy query results
- Access control logs

## Data Preprocessing

To create your own subset or modify the existing one:

1. **Install dependencies**:

   ```bash
   pip install pandas numpy scipy
   ```

2. **Run preprocessing script**:

   ```python
   from src.utils.data_loader import preprocess_mimic_subset
   
   # Preprocess MIMIC-III raw data
   subset = preprocess_mimic_subset(
       raw_data_path='data/raw/',
       output_path='data/processed/mimiciii_subset.csv',
       sample_size=1000
   )
   ```

## Privacy Considerations

⚠️ **Important**:

- The MIMIC-III dataset is already de-identified, but additional privacy-preserving techniques should still be applied when sharing or publishing results
- Never commit raw MIMIC-III files to version control
- Always follow your institution's IRB guidelines when working with health data
- Ensure compliance with HIPAA and other relevant privacy regulations

## Data Quality Notes

- Missing values are present in the dataset and should be handled appropriately
- Some patients may have multiple admissions
- Time series data requires temporal alignment for analysis
- Consider outliers and data validation steps before analysis

## References

1. Johnson, A. E. W., Pollard, T. J., Shen, L., Lehman, L. W. H., Feng, M., Ghassemi, M., Moody, B., Szolovits, P., Celi, L. A., & Mark, R. G. (2016). MIMIC-III, a freely accessible critical care database. Scientific Data, 3, 160035.

2. PhysioNet: <https://physionet.org/content/mimiciii/1.4/>

3. MIMIC-III Documentation: <https://mimic.mit.edu/docs/iii/>
