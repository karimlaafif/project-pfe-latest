```mermaid
graph TB
    subgraph "OLTP Layer (Operational)"
        PG[(PostgreSQL<br/>Prisma)]
        API[Next.js API<br/>Routes]
        UI[React UI<br/>Dashboard]
    end
    
    subgraph "Data Warehouse (Analytical)"
        subgraph "Bronze Layer - Raw Data"
            B1[(raw_loan_applications<br/>90-day TTL)]
            B2[(raw_fraud_transactions)]
            B3[(raw_economic_indicators)]
        end
        
        subgraph "Silver Layer - Cleaned Data"
            S1[(clean_loan_applications<br/>Feature Engineering)]
            S2[(fraud_patterns<br/>Aggregated)]
            S3[(economic_context)]
        end
        
        subgraph "Gold Layer - Business Analytics"
            G1[(portfolio_risk_monthly<br/>Materialized)]
            G2[(user_risk_clusters<br/>t-SNE 3D)]
            G3[(fraud_networks<br/>Graph Structure)]
        end
    end
    
    subgraph "ML Pipeline"
        TSNE[t-SNE Algorithm<br/>100D → 3D]
        LSTM[LSTM Neural Network<br/>Time-Series]
        BAYES[Bayesian Inference<br/>Probability Update]
    end
    
    subgraph "Visualization Layer"
        VIZ1[Three.js<br/>3D Risk Landscape]
        VIZ2[D3.js<br/>Force-Directed Graph]
        VIZ3[Recharts<br/>Time-Series Analytics]
    end
    
    %% Data Flow
    PG -->|ETL Extract| B1
    B1 -->|Transform + Clean| S1
    S1 -->|Aggregate| G1
    
    S1 -->|Features| TSNE
    TSNE -->|3D Coords| G2
    
    S1 -->|Sequences| LSTM
    LSTM -->|Predictions| S1
    
    S1 -->|Evidence| BAYES
    BAYES -->|Posterior Prob| S1
    
    G2 -->|Render| VIZ1
    G3 -->|Render| VIZ2
    G1 -->|Render| VIZ3
    
    VIZ1 --> UI
    VIZ2 --> UI
    VIZ3 --> UI
    
    style B1 fill:#8B4513
    style B2 fill:#8B4513
    style B3 fill:#8B4513
    style S1 fill:#C0C0C0
    style S2 fill:#C0C0C0
    style S3 fill:#C0C0C0
    style G1 fill:#FFD700
    style G2 fill:#FFD700
    style G3 fill:#FFD700
    style TSNE fill:#4169E1
    style LSTM fill:#4169E1
    style BAYES fill:#4169E1
```

# LendGuard AI Architecture Overview

## Data Flow Explanation

### 1. OLTP → Bronze (Extraction)
**Frequency:** Every 24 hours (configurable)
- PostgreSQL loan applications → `raw_loan_applications`
- IEEE-CIS fraud data → `raw_fraud_transactions`
- FRED economic API → `raw_economic_indicators`

**Retention:** 90 days (automatic TTL cleanup)

### 2. Bronze → Silver (Transformation)
**Processing:**
- Data quality scoring (0-100)
- Feature engineering:
  - `income_to_loan_ratio = income / loan_amount`
  - `employment_stability = months_employed / age`
- Risk categorization (LOW/MEDIUM/HIGH/CRITICAL)

**Retention:** 2 years

### 3. Silver → Gold (Aggregation)
**Business Logic:**
- Monthly portfolio risk summaries
- t-SNE dimension reduction (100D → 3D)
- Fraud network graph construction

**Retention:** Indefinite (archived after 5 years)

### 4. ML Pipeline Integration
- **t-SNE:** Runs during Silver → Gold transformation
- **LSTM:** Trained separately, predictions stored in Silver
- **Bayesian:** Real-time inference during API requests

### 5. Visualization Rendering
- **Three.js:** Reads `user_risk_clusters` (Gold layer)
- **D3.js:** Reads `fraud_networks` (Gold layer)
- **Recharts:** Reads `portfolio_risk_monthly` (Gold layer)

## Performance Characteristics

| Layer  | Storage Format | Query Speed | Use Case |
|--------|----------------|-------------|----------|
| Bronze | Row-oriented   | ~100ms      | Audit trail, raw backup |
| Silver | Column-oriented| ~20ms       | Feature engineering, ML training |
| Gold   | Aggregated     | ~5ms        | Dashboard visualization |

## Academic Concepts Applied

1. **Data Warehouse (Course):** Medallion architecture, OLTP vs OLAP separation
2. **Dimension Reduction (Course):** t-SNE algorithm for 3D projection
3. **Neural Networks (Course):** LSTM for time-series default prediction
4. **Mathematical Inference (Course):** Bayesian updating for probability
5. **Data Mining (Course):** Apriori algorithm for fraud patterns
6. **Visualization (Course):** 3D rendering with Three.js

---

**Created:** 2024-02-04  
**Version:** 2.0  
**Status:** Phase 1 Implementation Ready
