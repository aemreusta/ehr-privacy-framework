# Privacy-Preserving Strategies for Electronic Health Records

## Project Overview

This project explores privacy-preserving strategies for securing Electronic Health Records (EHRs) to mitigate risks while maintaining data integrity and utility. The growing use of EHRs has revolutionized healthcare, but increased digitization of sensitive health data has raised critical privacy concerns.

## Problem Definition

Unauthorized access to EHRs, data breaches, and misuse of personal health data can lead to severe consequences including identity theft, discrimination, and loss of trust in healthcare systems. This project develops strategies that enhance EHR security without compromising accessibility and efficiency.

## Motivation

The increasing number of cyberattacks on healthcare systems has led to significant privacy violations. This project aims to develop strategies that:

- Enhance EHR security
- Preserve patient trust in healthcare technologies
- Comply with legal and ethical standards
- Maintain data accessibility and efficiency

## Dataset

This project uses the **Medical Information Mart for Intensive Care (MIMIC-III)** dataset, a widely used dataset for research in health informatics containing de-identified health records including:

- Vital signs
- Medication information
- Clinical notes

## Methodology

Our integrated framework combines multiple privacy-preserving strategies:

### 1. Data Anonymization

- **k-anonymity**: Ensuring each record is indistinguishable from k-1 other records
- **l-diversity**: Ensuring well-represented values for sensitive attributes
- **t-closeness**: Ensuring the distribution of sensitive attributes is close to the overall distribution

### 2. Encryption Techniques

- **Homomorphic Encryption**: Allows computations on encrypted data without decryption

### 3. Access Control Models

- **Role-Based Access Control (RBAC)**: Fine-grained permissions based on user roles

### 4. Differential Privacy

- Adds noise to statistical analyses to prevent individual identification from aggregate results

## Project Structure

```
privacy_preserving_ehr/
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
│
├── data/
│   ├── README_DATA.md
│   ├── raw/                       # Original MIMIC-III files
│   ├── processed/
│   │   └── mimiciii_subset.csv    # Preprocessed subset for development
│   └── example_output/            # Example anonymized data
│
├── notebooks/                     # Jupyter notebooks for development and analysis
│   ├── 00_data_exploration.ipynb
│   ├── 01_anonymization_dev.ipynb
│   ├── 02_encryption_dev.ipynb
│   ├── 03_access_control_dev.ipynb
│   ├── 04_differential_privacy_dev.ipynb
│   └── 05_integrated_demo.ipynb
│
├── src/                           # Source code
│   ├── anonymization/            # Anonymization techniques
│   ├── encryption/               # Homomorphic encryption
│   ├── access_control/           # RBAC implementation
│   ├── differential_privacy/     # Differential privacy
│   ├── utils/                    # Common utilities
│   └── main.py                   # Main demonstration script
│
├── report/
│   └── technical_report.pdf
│
└── demo/                         # Demo video or link
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd privacy-preserve-mimic-iii
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Obtain MIMIC-III dataset:**
   - Follow the instructions in `data/README_DATA.md` to obtain the MIMIC-III dataset
   - Place the raw data in the `data/raw/` directory

## How to Run

### Quick Demo

```bash
python src/main.py
```

### Interactive Development

Use the Jupyter notebooks in the `notebooks/` directory:

```bash
jupyter notebook notebooks/
```

Start with `00_data_exploration.ipynb` for data exploration and proceed through the numbered notebooks.

### Individual Components

```bash
# Test anonymization
python -m src.anonymization.k_anonymity

# Test encryption
python -m src.encryption.homomorphic_encryption

# Test access control
python -m src.access_control.rbac

# Test differential privacy
python -m src.differential_privacy.dp_queries
```

## Usage Examples

### Data Anonymization

```python
from src.anonymization.k_anonymity import KAnonymity

anonymizer = KAnonymity(k=5)
anonymized_data = anonymizer.anonymize(data, quasi_identifiers=['age', 'zipcode'])
```

### Homomorphic Encryption

```python
from src.encryption.homomorphic_encryption import HomomorphicEncryption

he = HomomorphicEncryption()
encrypted_data = he.encrypt(sensitive_data)
result = he.compute_on_encrypted(encrypted_data, operation='sum')
```

### Access Control

```python
from src.access_control.rbac import RBAC

rbac = RBAC()
rbac.create_role('doctor', ['read_patient_data', 'write_notes'])
rbac.assign_user_role('dr_smith', 'doctor')
```

## Limitations

- Solutions focus primarily on data at rest and data in transit
- Real-time access monitoring is excluded
- Advanced ML-based anomaly detection is not implemented
- Evaluation limited to MIMIC-III dataset
- May not fully reflect challenges in real-world heterogeneous healthcare environments

## Novel Contribution

This project combines multiple privacy-preserving strategies (anonymization, encryption, access control, and differential privacy) into an integrated framework specifically for EHRs, providing a comprehensive solution that addresses various privacy concerns across different stages of data use.

## Demo Video

[Link to demo video will be provided here]

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- MIMIC-III dataset providers
- Privacy-preserving research community
- Healthcare informatics community

## Contact

For questions or collaborations, please open an issue on GitHub.
