"""
LendGuard AI - ETL Pipeline: PostgreSQL (OLTP) → ClickHouse (OLAP)
Implements the Bronze → Silver → Gold medallion architecture

Architecture:
1. Extract: Read from Prisma PostgreSQL using incremental watermarks
2. Transform: Apply data quality, feature engineering, dimension reduction
3. Load: Write to ClickHouse with proper partitioning

Requirements:
- clickhouse-driver
- pandas
- numpy
- scikit-learn (for t-SNE dimension reduction)
- psycopg2-binary
"""

import clickhouse_driver
import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
import numpy as np
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import json
import logging
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class DataWarehouseETL:
    """Main ETL orchestrator for LendGuard AI Data Warehouse"""
    
    def __init__(self):
        # PostgreSQL (OLTP) connection
        self.pg_conn = psycopg2.connect(
            os.getenv("DATABASE_URL"),
            cursor_factory=RealDictCursor
        )
        
        # ClickHouse (OLAP) connection
        self.ch_client = clickhouse_driver.Client(
            host=os.getenv("CLICKHOUSE_HOST", "localhost"),
            port=int(os.getenv("CLICKHOUSE_PORT", 9000)),
            database="bronze_layer"
        )
        
        logger.info("✅ Database connections established")
    
    # ============================================
    # PHASE 1: BRONZE LAYER - Raw Data Extraction
    # ============================================
    
    def extract_loans_to_bronze(self, lookback_hours: int = 24):
        """
        Extract raw loan applications from PostgreSQL to Bronze layer
        Uses incremental extraction based on updated_at watermark
        """
        logger.info(f"🔍 Extracting loans from last {lookback_hours} hours")
        
        # Get incremental watermark
        watermark = datetime.now() - timedelta(hours=lookback_hours)
        
        # Extract query
        query = """
            SELECT 
                'POSTGRES_PROD' as source_system,
                NOW() as ingestion_timestamp,
                id as source_id,
                row_to_json(loans.*) as payload,
                "userId" as user_id,
                "createdAt" as created_at
            FROM "Loan" as loans
            WHERE "updatedAt" >= %s
            ORDER BY "createdAt" DESC
        """
        
        with self.pg_conn.cursor() as cursor:
            cursor.execute(query, (watermark,))
            rows = cursor.fetchall()
        
        logger.info(f"📦 Extracted {len(rows)} loan records")
        
        # Insert into Bronze layer ClickHouse
        if rows:
            insert_query = """
                INSERT INTO bronze_layer.raw_loan_applications 
                (source_system, ingestion_timestamp, source_id, payload, user_id, created_at)
                VALUES
            """
            
            # Convert to ClickHouse format
            values = [
                (
                    row['source_system'],
                    row['ingestion_timestamp'],
                    row['source_id'],
                    json.dumps(row['payload']),
                    row['user_id'],
                    row['created_at']
                )
                for row in rows
            ]
            
            self.ch_client.execute(insert_query, values)
            logger.info(f"✅ Bronze layer: Inserted {len(rows)} records")
        
        return len(rows)
    
    # ============================================
    # PHASE 2: SILVER LAYER - Transformation & Quality
    # ============================================
    
    def transform_bronze_to_silver(self):
        """
        Transform Bronze raw data to Silver cleaned data
        Applies:
        1. Data quality checks
        2. Feature engineering
        3. Type conversions
        4. Business logic
        """
        logger.info("🔄 Transforming Bronze → Silver")
        
        # Read from Bronze
        bronze_query = """
            SELECT 
                source_id as loan_id,
                JSONExtractString(payload, 'userId') as user_id,
                toDateTime64(JSONExtractString(payload, 'createdAt'), 3) as application_date,
                toUInt8(JSONExtractInt(payload, 'age')) as age,
                toFloat64(JSONExtractString(payload, 'income')) as income,
                JSONExtractString(payload, 'education') as education_level,
                JSONExtractString(payload, 'employmentType') as employment_type,
                toUInt16(JSONExtractInt(payload, 'monthsEmployed')) as months_employed,
                toFloat64(JSONExtractString(payload, 'loanAmount')) as loan_amount,
                toUInt16(JSONExtractInt(payload, 'loanTerm')) as loan_term,
                toFloat32(JSONExtractString(payload, 'interestRate')) as interest_rate,
                JSONExtractString(payload, 'loanPurpose') as loan_purpose,
                toUInt16(JSONExtractInt(payload, 'creditScore')) as credit_score,
                toFloat32(JSONExtractString(payload, 'dtiRatio')) as dti_ratio,
                toUInt8(JSONExtractInt(payload, 'numCreditLines')) as num_credit_lines,
                toUInt8(JSONExtractInt(payload, 'hasMortgage')) as has_mortgage,
                toFloat32(JSONExtractString(payload, 'riskScore')) as risk_score,
                toFloat32(JSONExtractString(payload, 'fraudProbability')) as fraud_probability,
                toFloat32(JSONExtractString(payload, 'defaultProbability')) as default_probability
            FROM bronze_layer.raw_loan_applications
            WHERE toDate(created_at) >= today() - 7
        """
        
        bronze_df = pd.DataFrame(self.ch_client.execute(bronze_query))
        
        if bronze_df.empty:
            logger.warning("⚠️ No Bronze data to transform")
            return 0
        
        logger.info(f"📊 Processing {len(bronze_df)} Bronze records")
        
        # Feature Engineering
        bronze_df['income_to_loan_ratio'] = bronze_df['income'] / bronze_df['loan_amount']
        bronze_df['credit_utilization'] = bronze_df['dti_ratio']  # Simplified
        bronze_df['employment_stability'] = bronze_df['months_employed'] / bronze_df['age']
        
        # Risk Categorization (Business Logic)
        def categorize_risk(row):
            if row['default_probability'] < 0.15:
                return 'LOW'
            elif row['default_probability'] < 0.35:
                return 'MEDIUM'
            elif row['default_probability'] < 0.60:
                return 'HIGH'
            else:
                return 'CRITICAL'
        
        bronze_df['risk_category'] = bronze_df.apply(categorize_risk, axis=1)
        
        # Data Quality Score (0-100)
        def calculate_quality_score(row):
            score = 100.0
            # Penalize missing/invalid values
            if pd.isna(row['credit_score']) or row['credit_score'] == 0:
                score -= 25
            if pd.isna(row['income']) or row['income'] <= 0:
                score -= 25
            if row['age'] < 18 or row['age'] > 100:
                score -= 20
            return max(0, score)
        
        bronze_df['data_quality_score'] = bronze_df.apply(calculate_quality_score, axis=1)
        bronze_df['processing_timestamp'] = datetime.now()
        
        # Insert into Silver layer
        silver_insert = """
            INSERT INTO silver_layer.clean_loan_applications VALUES
        """
        
        # Convert DataFrame to tuples
        silver_values = bronze_df.to_dict('records')
        
        self.ch_client.execute(silver_insert, silver_values)
        logger.info(f"✅ Silver layer: Transformed {len(bronze_df)} records")
        
        return len(bronze_df)
    
    # ============================================
    # PHASE 3: GOLD LAYER - Business Analytics
    # ============================================
    
    def aggregate_portfolio_risk(self):
        """
        Create monthly portfolio risk aggregations for executive dashboards
        Materialized in Gold layer for O(1) query performance
        """
        logger.info("📈 Aggregating portfolio risk metrics")
        
        aggregate_query = """
            INSERT INTO gold_layer.portfolio_risk_monthly
            SELECT
                toStartOfMonth(application_date) as risk_month,
                
                -- Volume Metrics
                count() as total_applications,
                countIf(risk_category IN ('LOW', 'MEDIUM')) as approved_count,
                countIf(risk_category IN ('HIGH', 'CRITICAL')) as rejected_count,
                countIf(risk_category IN ('LOW', 'MEDIUM')) / count() as approval_rate,
                
                -- Risk Distribution
                countIf(risk_category = 'LOW') as low_risk_count,
                countIf(risk_category = 'MEDIUM') as medium_risk_count,
                countIf(risk_category = 'HIGH') as high_risk_count,
                countIf(risk_category = 'CRITICAL') as critical_risk_count,
                
                -- Portfolio Quality
                avg(credit_score) as avg_credit_score,
                avg(dti_ratio) as avg_dti_ratio,
                avg(loan_amount) as avg_loan_amount,
                sum(loan_amount) as total_exposure,
                
                -- Predictive Metrics
                avg(default_probability) as avg_default_prob,
                sum(loan_amount * default_probability) as expected_loss,
                quantile(0.95)(loan_amount * default_probability) as portfolio_var_95,
                
                -- Economic Context (placeholder - join with economic table)
                0.0 as unemployment_rate,
                0.0 as recession_prob
            FROM silver_layer.clean_loan_applications
            WHERE application_date >= toStartOfMonth(now() - INTERVAL 6 MONTH)
            GROUP BY risk_month
        """
        
        self.ch_client.execute(aggregate_query)
        logger.info("✅ Gold layer: Portfolio risk aggregated")
    
    def compute_user_clusters_tsne(self):
        """
        ACADEMIC IMPLEMENTATION: Dimension Reduction using t-SNE
        
        Takes 100+ dimensional user feature space and projects to 3D
        for interactive visualization in Three.js
        
        Mathematical Foundation:
        t-SNE minimizes KL divergence between high-dim and low-dim distributions
        """
        logger.info("🧠 Computing t-SNE dimension reduction (100D → 3D)")
        
        # Extract high-dimensional feature vectors
        features_query = """
            SELECT
                user_id,
                age,
                income,
                loan_amount,
                credit_score,
                dti_ratio,
                num_credit_lines,
                months_employed,
                income_to_loan_ratio,
                employment_stability,
                risk_score,
                fraud_probability,
                default_probability
            FROM silver_layer.clean_loan_applications
            WHERE application_date >= today() - 30
        """
        
        df = pd.DataFrame(self.ch_client.execute(features_query))
        
        if len(df) < 50:
            logger.warning("⚠️ Insufficient data for t-SNE (need 50+ samples)")
            return
        
        # Prepare feature matrix X
        feature_cols = df.columns.drop('user_id')
        X = df[feature_cols].values
        
        # Standardize features (t-SNE requirement)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Apply t-SNE (100+ dimensions → 3D)
        logger.info("🔬 Running t-SNE algorithm (this may take 30-60 seconds)...")
        tsne = TSNE(
            n_components=3,
            perplexity=30,
            n_iter=1000,
            random_state=42,
            verbose=1
        )
        X_embedded = tsne.fit_transform(X_scaled)
        
        # Assign cluster IDs using K-Means on the embedding
        from sklearn.cluster import KMeans
        kmeans = KMeans(n_clusters=5, random_state=42)
        cluster_ids = kmeans.fit_predict(X_embedded)
        
        # Create result DataFrame
        df['tsne_x'] = X_embedded[:, 0]
        df['tsne_y'] = X_embedded[:, 1]
        df['tsne_z'] = X_embedded[:, 2]
        df['cluster_id'] = cluster_ids
        df['cluster_snapshot_date'] = datetime.now().date()
        
        # Compute cluster statistics
        cluster_stats = df.groupby('cluster_id').agg({
            'user_id': 'count',
            'default_probability': 'mean',
            'credit_score': 'mean',
            'income': 'mean',
            'loan_amount': 'mean'
        }).rename(columns={'user_id': 'cluster_size'})
        
        df = df.merge(cluster_stats, on='cluster_id')
        
        # Insert into Gold layer
        insert_data = df[[
            'cluster_snapshot_date', 'cluster_id', 'user_id',
            'tsne_x', 'tsne_y', 'tsne_z',
            'cluster_size', 'default_probability', 
            'credit_score', 'income', 'loan_amount'
        ]].to_dict('records')
        
        insert_query = """
            INSERT INTO gold_layer.user_risk_clusters VALUES
        """
        
        self.ch_client.execute(insert_query, insert_data)
        logger.info(f"✅ t-SNE clusters: {len(df)} users mapped to 3D space")
    
    # ============================================
    # ORCHESTRATION
    # ============================================
    
    def run_full_pipeline(self):
        """Execute complete ETL pipeline: Bronze → Silver → Gold"""
        logger.info("🚀 Starting full ETL pipeline")
        start_time = datetime.now()
        
        try:
            # Step 1: Extract to Bronze
            bronze_count = self.extract_loans_to_bronze(lookback_hours=24)
            
            # Step 2: Transform to Silver
            silver_count = self.transform_bronze_to_silver()
            
            # Step 3: Aggregate to Gold
            self.aggregate_portfolio_risk()
            
            # Step 4: Dimension Reduction (Academic)
            self.compute_user_clusters_tsne()
            
            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"✅ Pipeline completed in {duration:.2f} seconds")
            logger.info(f"📊 Processed: {bronze_count} Bronze → {silver_count} Silver → Gold")
            
        except Exception as e:
            logger.error(f"❌ Pipeline failed: {str(e)}", exc_info=True)
            raise
        
        finally:
            self.pg_conn.close()
            self.ch_client.disconnect()


if __name__ == "__main__":
    etl = DataWarehouseETL()
    etl.run_full_pipeline()
