# Additional Datasets Required for LendGuard AI ML Pipeline

## Overview
This document outlines the 6 additional datasets required to power the full ML pipeline for LendGuard AI's enterprise features, including fraud detection, behavioral analytics, identity verification, compliance tracking, and portfolio risk assessment.

---

## 1. Fraud Transactions Dataset

### Purpose
Train fraud detection models separately from default prediction using real-world fraud patterns and behavioral anomalies.

### Specifications
- **Format:** CSV
- **Minimum Size:** 10,000+ transactions
- **Target Variable:** `IsFraud` (0 = Legitimate, 1 = Fraud)

### Required Columns
| Column Name | Type | Description |
|------------|------|-------------|
| TransactionID | String | Unique transaction identifier |
| ApplicantName | String | Name of the applicant |
| Email | String | Email address |
| PhoneNumber | String | Phone number |
| IPAddress | String | IP address of the request |
| DeviceID | String | Unique device fingerprint |
| Income | Float | Reported annual income |
| LoanAmount | Float | Requested loan amount |
| CreditScore | Int | Credit score (300-850) |
| NumRecentApplications | Int | Number of applications in last 30 days |
| AccountAge | Int | Age of account in days |
| GeolocationData | JSON | Lat/long coordinates |
| TimeOfApplication | DateTime | Timestamp of application |
| IsFraud | Int | **Target: 0 (legitimate) or 1 (fraud)** |

### Recommended Sources
1. **Kaggle: Credit Card Fraud Detection**
   - URL: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
   - Description: Real anonymized credit card transactions

2. **Kaggle: IEEE-CIS Fraud Detection**
   - URL: https://www.kaggle.com/c/ieee-fraud-detection
   - Description: Comprehensive fraud detection dataset from Vesta Corporation

3. **Kaggle: Synthetic Financial Datasets**
   - URL: https://www.kaggle.com/datasets/ealaxi/paysim1
   - Description: Synthetic mobile money transactions

4. **Generate Synthetic Data**
   - Use Python Faker library to generate realistic fraud patterns
   - Script: `scripts/generate_fraud_data.py`

---

## 2. Customer Behavior Dataset

### Purpose
Behavioral analytics and anomaly detection to identify suspicious user patterns (bot detection, velocity checks, session analysis).

### Specifications
- **Format:** CSV
- **Minimum Size:** 50,000+ events
- **Target Variable:** `IsBot` (0 = Human, 1 = Bot)

### Required Columns
| Column Name | Type | Description |
|------------|------|-------------|
| CustomerID | String | Unique customer identifier |
| SessionID | String | Unique session identifier |
| EventType | String | Type of event (click, scroll, form_fill, etc.) |
| Timestamp | DateTime | Event timestamp |
| DeviceType | String | mobile, desktop, tablet |
| Browser | String | Browser user agent |
| MouseMovements | Int | Number of mouse movements |
| KeystrokeDynamics | JSON | Typing speed and patterns |
| TimeSpent | Int | Time spent on page (seconds) |
| FormCompletionTime | Int | Time to complete form (seconds) |
| CopyPasteEvents | Int | Number of copy/paste actions |
| IsBot | Int | **Target: 0 (human) or 1 (bot)** |

### Recommended Sources
1. **Session Replay Tools**
   - Export data from LogRocket, FullStory, or Hotjar

2. **Kaggle: Web Behavior Analytics**
   - Search for user interaction and clickstream datasets

3. **Generate Synthetic Data**
   - Use behavioral modeling libraries
   - Script: `scripts/generate_behavioral_data.py`

---

## 3. Historical Loan Performance Dataset

### Purpose
Time-series analysis for portfolio risk assessment, stress testing, and macroeconomic correlation studies.

### Specifications
- **Format:** CSV
- **Minimum Size:** 5+ years of monthly data
- **Target Variable:** `LoanStatus` (Current, Defaulted, Paid Off, etc.)

### Required Columns
| Column Name | Type | Description |
|------------|------|-------------|
| LoanID | String | Unique loan identifier |
| OriginationDate | DateTime | Date loan was originated |
| MaturityDate | DateTime | Expected loan completion date |
| LoanAmount | Float | Original loan amount |
| InterestRate | Float | Annual interest rate (%) |
| MonthlyPayment | Float | Scheduled monthly payment |
| PaymentHistory | JSON | Array of payment amounts and dates |
| DaysDelinquent | Int | Total days delinquent |
| DefaultDate | DateTime | Date of default (if applicable) |
| RecoveryAmount | Float | Amount recovered after default |
| LoanStatus | String | **Current, Defaulted, Paid Off, Charged Off** |

### Recommended Sources
1. **Lending Club Open Data**
   - URL: https://www.lendingclub.com/info/download-data.action
   - Description: Historical peer-to-peer lending data

2. **Prosper Loan Data**
   - URL: https://www.prosper.com/Downloads/Services/Documentation/
   - Description: P2P lending platform data

3. **Freddie Mac Single-Family Loan-Level Dataset**
   - URL: https://www.freddiemac.com/research/datasets/sf-loanlevel-dataset
   - Description: Mortgage loan performance data

---

## 4. Identity Verification Dataset

### Purpose
Train document forgery detection models and identity verification systems using computer vision.

### Specifications
- **Format:** Images (JPG/PNG) + CSV metadata
- **Minimum Size:** 5,000+ documents
- **Target Variable:** `IsForgery` (0 = Authentic, 1 = Forged)

### Required Columns (Metadata CSV)
| Column Name | Type | Description |
|------------|------|-------------|
| DocumentID | String | Unique document identifier |
| DocumentType | String | ID, Passport, DriverLicense |
| ImagePath | String | Path to document image file |
| ExtractedText | String | OCR extracted text |
| IsForgery | Int | **Target: 0 (authentic) or 1 (forged)** |
| ForgeryType | String | Type of forgery detected |
| ConfidenceScore | Float | Verification confidence (0-1) |

### Recommended Sources
1. **Kaggle: Document Classification**
   - Search for ID verification and document analysis datasets

2. **RVL-CDIP Dataset**
   - URL: https://www.cs.cmu.edu/~aharley/rvl-cdip/
   - Description: 400,000+ grayscale images of documents

3. **Generate Synthetic Forgeries**
   - Use GANs (Generative Adversarial Networks) to create realistic forgeries
   - Tools: StyleGAN, DALL-E fine-tuning

---

## 5. Compliance Audit Dataset

### Purpose
Track compliance violations, audit findings, and remediation timelines for GRC dashboards.

### Specifications
- **Format:** CSV
- **Minimum Size:** 1,000+ audit records
- **Target Variable:** `Status` (Open, Remediated, Closed)

### Required Columns
| Column Name | Type | Description |
|------------|------|-------------|
| AuditID | String | Unique audit identifier |
| AuditDate | DateTime | Date of audit |
| Framework | String | GDPR, SOC2, ISO27001, PCI_DSS, etc. |
| Finding | String | Description of the finding |
| Severity | String | LOW, MEDIUM, HIGH, CRITICAL |
| Status | String | **OPEN, IN_PROGRESS, REMEDIATED, CLOSED** |
| RemediationDate | DateTime | Date finding was remediated |
| ResponsibleTeam | String | Team responsible for remediation |

### Recommended Sources
1. **Manually Create Based on Common Findings**
   - Reference GDPR, SOC 2, ISO 27001 compliance checklists

2. **Compliance Framework Documentation**
   - Extract common audit findings from official standards

3. **Generate Synthetic Audit Data**
   - Script: `scripts/generate_compliance_audit_data.py`

---

## 6. Economic Indicators Dataset

### Purpose
Macroeconomic risk factors for portfolio stress testing and recession scenario modeling.

### Specifications
- **Format:** CSV (Time-series)
- **Minimum Size:** 10+ years of monthly data

### Required Columns
| Column Name | Type | Description |
|------------|------|-------------|
| Date | DateTime | Month-year (YYYY-MM-01) |
| UnemploymentRate | Float | National unemployment rate (%) |
| GDP_Growth | Float | GDP growth rate (%) |
| InflationRate | Float | Consumer Price Index change (%) |
| InterestRate | Float | Federal funds rate (%) |
| HousingPriceIndex | Float | National housing price index |
| ConsumerConfidence | Float | Consumer confidence index |
| DefaultRate | Float | National loan default rate (%) |

### Recommended Sources
1. **Federal Reserve Economic Data (FRED)**
   - URL: https://fred.stlouisfed.org/
   - API: Yes (free)
   - Description: Comprehensive US economic data

2. **World Bank Open Data**
   - URL: https://data.worldbank.org/
   - Description: Global economic indicators

3. **IMF Data**
   - URL: https://www.imf.org/en/Data
   - Description: International economic data

4. **Bureau of Labor Statistics**
   - URL: https://www.bls.gov/data/
   - Description: US labor market statistics

---

## Implementation Guide

### Step 1: Download Datasets
```bash
# Create datasets directory
mkdir -p dataset

# Download from Kaggle (requires Kaggle API)
kaggle datasets download -d mlg-ulb/creditcardfraud -p dataset/
kaggle datasets download -d ealaxi/paysim1 -p dataset/

# Download Lending Club data
# Manual download from: https://www.lendingclub.com/info/download-data.action

# Fetch FRED API data
python scripts/fetch_fred_data.py
```

### Step 2: Data Preprocessing
```bash
# Run preprocessing scripts
python scripts/preprocess_fraud_data.py
python scripts/preprocess_behavioral_data.py
python scripts/preprocess_loan_performance.py
```

### Step 3: Train ML Models
```bash
# Train fraud detection model
python scripts/train_fraud_model.py

# Train default prediction model
python scripts/train_default_model.py

# Train anomaly detection model
python scripts/train_anomaly_detector.py
```

### Step 4: Model Deployment
```bash
# Export models for Next.js API integration
python scripts/export_models.py

# Copy models to API directory
cp models/*.pkl app/api/ml-models/
```

---

## Data Storage Recommendations

### Development
- Store datasets in `dataset/` directory
- Add `dataset/` to `.gitignore` (datasets can be large)
- Use relative paths in scripts

### Production
- Store datasets in AWS S3, Google Cloud Storage, or Azure Blob Storage
- Use signed URLs for secure access
- Implement data retention policies (GDPR compliance)

### Database
- Store metadata and predictions in PostgreSQL
- Use Prisma ORM for type-safe queries
- Implement audit logging for all ML predictions

---

## Next Steps

1. ✅ Download Dataset 1 (Fraud Transactions)
2. ✅ Download Dataset 2 (Customer Behavior)
3. ✅ Download Dataset 3 (Historical Loan Performance)
4. ⬜ Download Dataset 4 (Identity Verification)
5. ⬜ Download Dataset 5 (Compliance Audits) - Generate synthetic
6. ✅ Download Dataset 6 (Economic Indicators) - FRED API

**Priority:** Start with Datasets 1, 2, and 6 for immediate ML pipeline value.
