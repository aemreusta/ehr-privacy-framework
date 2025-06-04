# Privacy-Preserving EHR Framework Demo

This directory contains demonstration materials and quick-start guides for the privacy-preserving EHR framework.

## Quick Start Demo

### 1. Process Raw Data and Run Complete Analysis

```bash
# From the project root directory
python src/main.py
```

This will:

- Process raw MIMIC-III data
- Apply k-anonymity with multiple privacy levels
- Generate comprehensive privacy-utility analysis
- Demonstrate role-based access control
- Save all results to `data/example_output/`

### 2. Interactive Analysis

```bash
# Start Jupyter notebook for interactive exploration
jupyter notebook notebooks/01_data_exploration_and_anonymization.ipynb
```

## Generated Outputs

After running the demo, you'll find:

### Processed Data

- `data/processed/mimic_comprehensive_dataset.csv` - Processed MIMIC-III dataset
- `data/processed/data_processing_summary.txt` - Processing statistics

### Anonymized Datasets

- `data/example_output/anonymized/k2_anonymized_comprehensive.csv`
- `data/example_output/anonymized/k3_anonymized_comprehensive.csv`
- `data/example_output/anonymized/k5_anonymized_comprehensive.csv`
- `data/example_output/anonymized/k10_anonymized_comprehensive.csv`

### Analysis Reports

- `data/example_output/privacy_utility_report.txt` - Privacy-utility metrics
- `data/example_output/comprehensive_summary.json` - Complete analysis summary
- `data/example_output/implementation_recommendations.md` - Deployment guide

### Visualizations

- `data/example_output/plots/data_exploration.png` - Data distribution plots
- `data/example_output/plots/privacy_utility_analysis.png` - Trade-off analysis

### Access Control

- `data/example_output/access_control_log.csv` - RBAC simulation results
- `data/example_output/rbac_compliance_report.txt` - Compliance analysis

## Key Features Demonstrated

1. **Real Data Processing**: Uses authentic MIMIC-III clinical data
2. **Multi-level Privacy**: k-anonymity with k=2,3,5,10
3. **Utility Analysis**: Comprehensive privacy-utility trade-off evaluation
4. **Access Control**: Healthcare role-based permissions
5. **Scalable Architecture**: Modular design for easy extension

## Performance Metrics

The demo typically processes:

- 129 patient admission records
- 24 clinical variables
- 4 anonymization levels
- Complete analysis in ~15 seconds

## Next Steps

1. Review the generated reports in `data/example_output/`
2. Experiment with different k-values using the notebook
3. Extend the framework with additional privacy techniques
4. Deploy in your healthcare environment with appropriate safeguards
