-- ============================================
-- LendGuard AI Data Warehouse Schema (v2.0)
-- Medallion Architecture: Bronze → Silver → Gold
-- Database: ClickHouse (Column-Oriented OLAP)
-- ============================================

-- ============================================
-- BRONZE LAYER: Raw Data Landing Zone
-- ============================================
-- Purpose: Exact copy of source systems with minimal transformation
-- Retention: 90 days rolling window

CREATE DATABASE IF NOT EXISTS bronze_layer;

-- Raw Loan Applications (from Prisma Loan table)
CREATE TABLE bronze_layer.raw_loan_applications (
    -- Source Identifiers
    source_system       String,
    ingestion_timestamp DateTime64(3) DEFAULT now64(3),
    source_id           String,
    
    -- Raw JSON payload (entire Prisma Loan object)
    payload             String,
    
    -- Extraction for indexing
    user_id             String,
    created_at          DateTime64(3),
    
    -- Partitioning
    partition_date      Date MATERIALIZED toDate(created_at)
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(partition_date)
ORDER BY (partition_date, created_at, source_id)
TTL partition_date + INTERVAL 90 DAY;

-- Raw Fraud Transactions (from IEEE-CIS dataset)
CREATE TABLE bronze_layer.raw_fraud_transactions (
    ingestion_timestamp DateTime64(3) DEFAULT now64(3),
    transaction_id      String,
    payload             String,  -- Raw CSV row as JSON
    is_fraud            UInt8,
    transaction_dt      DateTime64(3),
    partition_date      Date MATERIALIZED toDate(transaction_dt)
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(partition_date)
ORDER BY (partition_date, transaction_dt, transaction_id)
TTL partition_date + INTERVAL 90 DAY;

-- Raw Economic Indicators (from FRED API)
CREATE TABLE bronze_layer.raw_economic_indicators (
    ingestion_timestamp DateTime64(3) DEFAULT now64(3),
    indicator_date      Date,
    indicator_type      String,
    raw_value           Float64,
    source_api          String,
    metadata            String  -- JSON metadata
) ENGINE = MergeTree()
ORDER BY (indicator_date, indicator_type);


-- ============================================
-- SILVER LAYER: Cleaned and Conformed Data
-- ============================================
-- Purpose: Business-ready data with quality checks applied
-- Retention: 2 years

CREATE DATABASE IF NOT EXISTS silver_layer;

-- Cleaned Loan Applications with Feature Engineering
CREATE TABLE silver_layer.clean_loan_applications (
    -- Primary Keys
    loan_id             String,
    user_id             String,
    application_date    DateTime64(3),
    
    -- Applicant Demographics
    age                 UInt8,
    income              Float64,
    education_level     Enum8('HIGH_SCHOOL' = 1, 'BACHELOR' = 2, 'MASTER' = 3, 'PHD' = 4),
    employment_type     Enum8('FULL_TIME' = 1, 'PART_TIME' = 2, 'SELF_EMPLOYED' = 3, 'UNEMPLOYED' = 4),
    months_employed     UInt16,
    
    -- Loan Characteristics
    loan_amount         Float64,
    loan_term           UInt16,
    interest_rate       Float32,
    loan_purpose        String,
    
    -- Risk Factors
    credit_score        UInt16,
    dti_ratio           Float32,
    num_credit_lines    UInt8,
    has_mortgage        UInt8,
    
    -- Engineered Features (computed during ETL)
    income_to_loan_ratio    Float32,
    credit_utilization      Float32,
    employment_stability    Float32,  -- months_employed / age ratio
    risk_category           Enum8('LOW' = 1, 'MEDIUM' = 2, 'HIGH' = 3, 'CRITICAL' = 4),
    
    -- ML Predictions (from OLTP system)
    risk_score              Float32,
    fraud_probability       Float32,
    default_probability     Float32,
    
    -- Metadata
    data_quality_score      Float32,
    processing_timestamp    DateTime64(3) DEFAULT now64(3),
    partition_date          Date MATERIALIZED toDate(application_date)
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(partition_date)
ORDER BY (partition_date, application_date, loan_id)
TTL partition_date + INTERVAL 730 DAY;  -- 2 years retention

-- Aggregated Fraud Patterns
CREATE TABLE silver_layer.fraud_patterns (
    pattern_id          String,
    detection_date      DateTime64(3),
    
    -- Pattern Characteristics
    ip_address          String,
    device_fingerprint  String,
    email_domain        String,
    application_hour    UInt8,
    
    -- Aggregated Metrics
    total_applications  UInt32,
    fraud_count         UInt32,
    fraud_rate          Float32,
    avg_loan_amount     Float64,
    
    -- Clustering Results (from t-SNE)
    cluster_id          UInt16,
    cluster_centroid_x  Float32,
    cluster_centroid_y  Float32,
    cluster_centroid_z  Float32,
    
    partition_date      Date MATERIALIZED toDate(detection_date)
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(partition_date)
ORDER BY (partition_date, fraud_rate DESC, pattern_id);

-- Time-Series Economic Context
CREATE TABLE silver_layer.economic_context (
    context_date        Date,
    
    -- Macroeconomic Indicators
    unemployment_rate   Float32,
    gdp_growth_yoy      Float32,
    inflation_rate      Float32,
    fed_funds_rate      Float32,
    housing_price_index Float32,
    consumer_confidence Float32,
    
    -- Derived Recession Signals
    recession_probability Float32,  -- From Bayesian model
    credit_stress_index   Float32,  -- Composite score
    
    PRIMARY KEY (context_date)
) ENGINE = ReplacingMergeTree(context_date)
ORDER BY context_date;


-- ============================================
-- GOLD LAYER: Business-Ready Analytics Tables
-- ============================================
-- Purpose: Optimized for specific business questions
-- Retention: Indefinite (with archiving policy)

CREATE DATABASE IF NOT EXISTS gold_layer;

-- Portfolio Risk Dashboard (aggregated by month)
CREATE TABLE gold_layer.portfolio_risk_monthly (
    risk_month          Date,
    
    -- Volume Metrics
    total_applications  UInt32,
    approved_count      UInt32,
    rejected_count      UInt32,
    approval_rate       Float32,
    
    -- Risk Distribution
    low_risk_count      UInt32,
    medium_risk_count   UInt32,
    high_risk_count     UInt32,
    critical_risk_count UInt32,
    
    -- Portfolio Quality
    avg_credit_score    Float32,
    avg_dti_ratio       Float32,
    avg_loan_amount     Float64,
    total_exposure      Float64,  -- Sum of all loan amounts
    
    -- Predictive Metrics
    avg_default_prob    Float32,
    expected_loss       Float64,  -- Total exposure * avg_default_prob
    portfolio_var_95    Float64,  -- Value at Risk (95% confidence)
    
    -- Economic Context (denormalized for performance)
    unemployment_rate   Float32,
    recession_prob      Float32,
    
    PRIMARY KEY (risk_month)
) ENGINE = SummingMergeTree()
ORDER BY risk_month;

-- User Behavior Cohorts (for Dimension Reduction visualization)
CREATE TABLE gold_layer.user_risk_clusters (
    cluster_snapshot_date Date,
    cluster_id            UInt16,
    user_id               String,
    
    -- t-SNE Coordinates (3D projection of 100+ features)
    tsne_x                Float32,
    tsne_y                Float32,
    tsne_z                Float32,
    
    -- Cluster Statistics
    cluster_size          UInt32,
    cluster_avg_default   Float32,
    cluster_risk_level    Enum8('LOW' = 1, 'MEDIUM' = 2, 'HIGH' = 3, 'CRITICAL' = 4),
    
    -- Representative Features
    avg_credit_score      Float32,
    avg_income            Float64,
    avg_loan_amount       Float64,
    
    PRIMARY KEY (cluster_snapshot_date, cluster_id, user_id)
) ENGINE = ReplacingMergeTree(cluster_snapshot_date)
PARTITION BY toYYYYMM(cluster_snapshot_date)
ORDER BY (cluster_snapshot_date, cluster_id, user_id);

-- Fraud Network Graph (for Force-Directed visualization)
CREATE TABLE gold_layer.fraud_networks (
    detection_date      Date,
    network_id          String,
    
    -- Graph Structure
    node_id             String,  -- User or entity ID
    node_type           Enum8('USER' = 1, 'IP' = 2, 'DEVICE' = 3, 'EMAIL' = 4),
    
    -- Edges (connections)
    connected_nodes     Array(String),
    edge_weights        Array(Float32),  -- Strength of connection
    
    -- Network Metrics
    degree_centrality   Float32,  -- How many connections
    betweenness_central Float32,  -- Bridge between communities
    is_hub_node         UInt8,    -- Flag for central fraud organizers
    
    -- Risk Scoring
    fraud_confidence    Float32,
    total_fraud_amount  Float64,
    
    PRIMARY KEY (detection_date, network_id, node_id)
) ENGINE = ReplacingMergeTree(detection_date)
PARTITION BY toYYYYMM(detection_date)
ORDER BY (detection_date, fraud_confidence DESC, network_id);


-- ============================================
-- MATERIALIZED VIEWS: Real-Time Aggregations
-- ============================================

-- Real-time Risk Score Distribution
CREATE MATERIALIZED VIEW gold_layer.mv_realtime_risk_distribution
ENGINE = AggregatingMergeTree()
PARTITION BY toYYYYMM(application_date)
ORDER BY (application_date, risk_category)
AS SELECT
    toDate(application_date) as application_date,
    risk_category,
    count() as application_count,
    avg(risk_score) as avg_risk_score,
    sum(loan_amount) as total_exposure
FROM silver_layer.clean_loan_applications
GROUP BY application_date, risk_category;

-- Daily Fraud Rate Monitoring
CREATE MATERIALIZED VIEW gold_layer.mv_daily_fraud_rate
ENGINE = SummingMergeTree()
ORDER BY fraud_date
AS SELECT
    toDate(detection_date) as fraud_date,
    sum(fraud_count) as total_frauds,
    sum(total_applications) as total_applications,
    avg(fraud_rate) as avg_fraud_rate
FROM silver_layer.fraud_patterns
GROUP BY fraud_date;


-- ============================================
-- ANALYTICS FUNCTIONS (User-Defined)
-- ============================================

-- Bayesian Posterior Probability Calculator
CREATE FUNCTION bayesian_default_prob AS (prior, evidence_quality, observed_default_rate) -> 
    (prior * observed_default_rate) / 
    ((prior * observed_default_rate) + ((1 - prior) * (1 - observed_default_rate)));

-- Portfolio Value-at-Risk (95% confidence)
CREATE FUNCTION portfolio_var_95 AS (exposures, default_probs) -> 
    quantile(0.95)(arrayMap((x, p) -> x * p, exposures, default_probs));
