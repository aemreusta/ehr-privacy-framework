# Project Methodology

**AIN413 Machine Learning For Healthcare - Course Project**  
**Hacettepe University - Department of Artificial Intelligence Engineering**  
**Spring Semester 2025**

---

**Student:** Ahmet Emre Usta  
**Student ID:** 2200765036  
**Instructor:** Asst. Prof. Gülden Olgun  

---

## Project Definition

**Title:** Privacy-Preserving Strategies for Electronic Health Records

## Problem Definition

The growing use of electronic health records (EHRs) has revolutionized healthcare by providing accessible, efficient, and accurate patient data management. However, with the increased digitization of sensitive health data, privacy concerns have become a critical issue. Unauthorized access to EHRs, data breaches, and misuse of personal health data can lead to severe consequences, including identity theft, discrimination, and loss of trust in healthcare systems. This project explores privacy-preserving strategies for securing EHRs to mitigate these risks while maintaining the integrity and utility of the data.

## Motivation

The increasing number of cyberattacks on healthcare systems has led to significant privacy violations. The sensitive nature of health data, combined with the growing trend of sharing data across platforms, increases the risk of exposure. Developing and evaluating privacy-preserving techniques is essential not only to comply with legal and ethical standards, but also to preserve patient trust in healthcare technologies. This project aims to develop strategies that enhance EHR security without compromising the accessibility and efficiency that make electronic health records so valuable.

## Dataset

For this project, I will use publicly available EHR datasets such as the Medical Information Mart for Intensive Care (MIMIC-III), a widely used dataset for research in health informatics. MIMIC-III contains de-identified health records, making it suitable for developing privacy-preserving methodologies. The dataset includes vital signs, medication information, and clinical notes, providing a comprehensive view of patient health data.

### Dataset Characteristics

- **Total Records**: 129 patient admissions
- **Unique Patients**: 100 individuals  
- **Data Dimensions**: 24 clinical variables
- **Data Types**: Demographics, vital signs, laboratory values, diagnoses, medications
- **Time Period**: Derived from ICU stays

## Proposed Methodology

### 1. Data Anonymization

Apply techniques such as k-anonymity, l-diversity, and t-closeness to anonymize sensitive data, thereby ensuring that patient identities remain protected while maintaining the utility of the data.

**Implementation:**

- **k-anonymity**: Ensuring each record is indistinguishable from at least k-1 others
- **l-diversity**: Requiring diversity in sensitive attributes within equivalence classes
- **t-closeness**: Distribution privacy with Earth Mover's Distance calculations
- **Quasi-identifiers**: age, gender, admission_type, ethnicity
- **Sensitive attributes**: primary_diagnosis, mortality

### 2. Encryption Techniques

Implement encryption protocols, such as homomorphic encryption, which allows computations on encrypted data without decrypting it and ensuring privacy during analysis.

**Implementation:**

- **CKKS Scheme**: Floating-point arithmetic on encrypted data using Pyfhel
- **Supported Operations**: Homomorphic addition, multiplication, secure aggregation
- **Healthcare Applications**: Secure multi-institutional analytics

### 3. Access Control Models

Design role-based access control (RBAC) systems with fine-grained permissions to restrict access to sensitive data based on user roles, ensuring that only authorized personnel can access specific patient data.

**Implementation:**

- **Healthcare-specific roles**: 7 roles from researchers to system administrators
- **Fine-grained permissions**: 23 distinct permission types
- **Compliance monitoring**: Automated access logging and audit trails

### 4. Differential Privacy

Incorporate differential privacy techniques to add noise to statistical analyses, ensuring that individuals' data cannot be identified from aggregate results.

**Implementation:**

- **Laplace Mechanism**: Adding calibrated noise to statistical queries
- **Privacy Budget (ε)**: Tested with values 0.1, 0.5, 1.0, 2.0
- **Query Types**: Count, mean, histogram, correlation queries

## Limitations

Due to the project's scope, the proposed solutions will focus primarily on protecting data at rest and data in transit. Real-time access monitoring and advanced machine learning-based anomaly detection will be excluded. Additionally, the evaluation will be limited to the MIMIC-III dataset and may not fully reflect the challenges in deploying these techniques in real-world heterogeneous healthcare environments.

### Specific Limitations Addressed

- Focus on static data privacy rather than real-time monitoring
- Limited to MIMIC-III dataset characteristics
- Computational overhead considerations for large-scale deployment
- Balance between privacy protection and clinical utility

## Novel Contribution

Although several studies have explored privacy-preserving techniques in healthcare, this project aims to combine multiple strategies (anonymization, encryption, access control, and differential privacy) into an integrated framework specifically for EHRs. By evaluating the effectiveness of these techniques in a single system, the project provides a comprehensive solution that addresses various privacy concerns across different stages of data use.

### Key Innovations

1. **Integrated Multi-Technique Framework**: First comprehensive integration of k-anonymity, l-diversity, t-closeness, differential privacy, and homomorphic encryption
2. **Healthcare-Specific Implementation**: Specialized for EHR data characteristics and clinical workflows
3. **Comprehensive Evaluation**: Systematic analysis of privacy-utility trade-offs across all techniques
4. **Production-Ready Solution**: Practical framework tested on real clinical data
5. **Regulatory Compliance**: Addressing HIPAA, GDPR, and FDA requirements

## Expected Outcomes

1. **Privacy Protection**: Achieve >90% privacy score through multi-layer protection
2. **Data Utility**: Maintain >80% data utility for clinical analysis
3. **Processing Efficiency**: Real-time processing (<5 seconds) for privacy pipeline
4. **Regulatory Compliance**: Full compliance with healthcare data protection standards
5. **Framework Reusability**: Extensible architecture for future healthcare applications

## Evaluation Metrics

### Privacy Metrics

- Suppression rates for anonymization techniques
- Privacy budget consumption for differential privacy
- Distribution compliance for t-closeness
- Access control audit success rates

### Utility Metrics  

- Data retention rates after privacy protection
- Statistical property preservation
- Clinical analysis accuracy
- Query result precision

### Performance Metrics

- Processing time for each privacy technique
- Memory usage and computational overhead
- Scalability with varying dataset sizes
- Framework integration efficiency

---

**Course:** AIN413 Machine Learning For Healthcare  
**Institution:** Hacettepe University  
**Department:** Artificial Intelligence Engineering  
**Semester:** Spring 2025
