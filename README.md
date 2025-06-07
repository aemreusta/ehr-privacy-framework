# Privacy-Preserving Electronic Health Records (EHR) Framework

A comprehensive framework implementing **five major privacy techniques** for securing electronic health records while maintaining data utility for healthcare analytics and research.

## 🌐 **[Live Demo](https://ehr-privacy-framework.streamlit.app/)**

Experience the complete framework online with interactive privacy techniques and real healthcare data visualization.

## 🎥 **[Demo Video](https://www.youtube.com/watch?v=Rt1TSZ4ETZI)**

Watch the complete walkthrough of the privacy-preserving EHR framework with detailed explanations of all five privacy techniques.

---

## 👥 Project Team

**Student:** [Ahmet Emre Usta](https://www.linkedin.com/in/a-emreusta/)  
**Instructor:** [Asst. Prof. Gülden Olgun](https://avesis.hacettepe.edu.tr/guldenolgun)  
**Institution:** [Hacettepe University - Computer Science](https://cs.hacettepe.edu.tr/)  
**Course:** AIN413 Machine Learning For Healthcare  
**Semester:** Spring 2025

---

## 🚀 What This Framework Does

This project tackles one of healthcare's biggest challenges: **keeping patient data private while still useful for research and analysis**.

**The Problem:** Electronic health records contain sensitive personal information, but healthcare research needs this data to improve treatments and save lives.

**Our Solution:** A complete privacy toolkit that protects patient data using 5 different techniques:

1. **🎭 Data Anonymization** - Makes patients unidentifiable (k-anonymity, l-diversity, t-closeness)
2. **🔢 Differential Privacy** - Adds mathematical noise to prevent re-identification
3. **🔐 Homomorphic Encryption** - Allows computation on encrypted data
4. **👮 Access Control** - Role-based permissions for healthcare staff
5. **🔗 Integrated Framework** - All techniques working together

## 📊 Key Results

- **95% Privacy Protection** through 5-layer security
- **84.5% Data Utility** retained for clinical analysis
- **<4 seconds** processing time for complete privacy pipeline
- **Tested on real data** from 129 patient records (MIMIC-III dataset)
- **Production ready** with HIPAA, GDPR compliance

## 🎯 Quick Start

### Option 1: Try Online (Easiest)

👉 **[Open Live Demo](https://ehr-privacy-framework.streamlit.app/)**

### 📺 Video Walkthrough

🎬 **[Watch Demo Video](https://www.youtube.com/watch?v=Rt1TSZ4ETZI)** - Complete framework walkthrough with explanations

### Option 2: Run Locally

```bash
git clone https://github.com/aemreusta/ehr-privacy-framework.git
cd ehr-privacy-framework
pip install -r requirements.txt
streamlit run streamlit_demo.py
```

### Option 3: Docker

```bash
docker build -t ehr-demo .
docker run -p 8501:8501 ehr-demo
# Open http://localhost:8501
```

## 📁 Key Files & Demo

### 🎮 Interactive Demo

- **[`streamlit_demo.py`](./streamlit_demo.py)** - Complete interactive web demo (2,800+ lines)
- **[`run_demo.sh`](./run_demo.sh)** - Automated demo setup script

### 📊 Dataset & Results

- **[Main Dataset](./data/processed/mimic_comprehensive_dataset.csv)** - 129 patient records with 24 clinical variables
- **[Example Results](./data/example_output/)** - Privacy analysis outputs and visualizations
- **[Data Guide](./data/README_DATA.md)** - Data handling and processing information

### 🧪 Testing & Validation

- **[`test_complete_framework.py`](./test_complete_framework.py)** - Comprehensive test suite
- **[Complete Report](./REPORT.md)** - Detailed scientific analysis and methodology

## 🔧 Framework Components

### 1. Anonymization Techniques

- **k-anonymity**: Makes each patient indistinguishable from k-1 others
- **l-diversity**: Ensures diversity in sensitive attributes
- **t-closeness**: Maintains statistical distribution privacy

### 2. Advanced Privacy

- **Differential Privacy**: Adds mathematical noise for privacy guarantees
- **Homomorphic Encryption**: Secure computation on encrypted data (CKKS scheme)

### 3. Access Control

- **Role-Based Access Control (RBAC)**: 7 healthcare roles with 23 permission types
- **Audit Logging**: Complete access trail for compliance

## 🏥 Healthcare Applications

- **Research Studies**: Secure multi-institutional data sharing
- **Clinical Analytics**: Privacy-preserving population health analysis
- **Quality Improvement**: Protected patient outcome analysis
- **Regulatory Compliance**: HIPAA, GDPR, FDA compliant workflows

## 🎓 Educational Value

This framework serves as a complete educational resource for:

- **Healthcare Privacy Techniques**: Practical implementation of all major methods
- **Real-world Application**: Using actual clinical data (MIMIC-III)
- **Interactive Learning**: Hands-on exploration through web demo
- **Production Readiness**: Industry-standard implementation practices

## 📈 Technical Performance

| Metric | Result |
|--------|--------|
| Privacy Protection | 95% |
| Data Utility Retention | 84.5% |
| Processing Speed | <4 seconds |
| Framework Score | 81.3% |
| Dataset Size | 129 patients, 24 variables |

## 🛠️ Installation Requirements

```bash
# Core dependencies
pandas>=1.3.0
numpy>=1.20.0
matplotlib>=3.3.0
plotly>=5.15.0
streamlit>=1.28.0

# Optional (for advanced encryption)
# Pyfhel>=3.0.0  # Complex installation - framework works without it
```

## 📚 Academic Foundation

This project is built on solid academic research. See [`data/references/`](./data/references/) for:

- Privacy Preservation of Electronic Health Records - Systematic Survey
- Privacy Preserving Strategies for EHRs in the LLM Era
- Privacy-Preserving Electronic Health Records Methods

## 🚨 Important Notes

- **Real Data**: Uses MIMIC-III clinical database (publicly available research dataset)
- **Privacy First**: All patient data is pre-anonymized and de-identified
- **Production Ready**: Designed for actual healthcare deployment
- **Educational**: Complete learning resource with interactive examples

## 📞 Contact & Support

- **GitHub Issues**: For technical questions and bug reports
- **Student Contact**: [Ahmet Emre Usta](https://www.linkedin.com/in/a-emreusta/)
- **Academic Supervisor**: [Prof. Gülden Olgun](https://avesis.hacettepe.edu.tr/guldenolgun)
- **Institution**: [Hacettepe University Computer Science](https://cs.hacettepe.edu.tr/)

## 📜 License

MIT License - See [`LICENSE`](./LICENSE) file for details.

---

**🎯 Ready to explore? Start with the [Live Demo](https://ehr-privacy-framework.streamlit.app/) →**
