# LendGuard AI - Phase 1 Implementation Guide
## Data Warehouse Foundation Setup

### Prerequisites
- Python 3.11+
- PostgreSQL (existing - via Prisma)
- ClickHouse Server (to be installed)
- Node.js 18+ (existing)

---

## Step 1: Install ClickHouse Server

### Windows (PowerShell as Administrator):
```powershell
# Download ClickHouse installer
Invoke-WebRequest -Uri https://builds.clickhouse.com/master/amd64/clickhouse-common-static-23.8.1.0.zip -OutFile clickhouse.zip
Expand-Archive -Path clickhouse.zip -DestinationPath C:\ClickHouse
cd C:\ClickHouse

# Start ClickHouse server
.\clickhouse-server.exe
```

### Alternative: Docker (Recommended)
```bash
# Pull ClickHouse image
docker pull clickhouse/clickhouse-server:latest

# Run ClickHouse container
docker run -d \
  --name lendguard-warehouse \
  -p 8123:8123 \
  -p 9000:9000 \
  --ulimit nofile=262144:262144 \
  clickhouse/clickhouse-server:latest
```

Verify installation:
```bash
curl http://localhost:8123
# Should return: Ok.
```

---

## Step 2: Create Warehouse Schema

Navigate to project directory:
```bash
cd "C:\Users\PC\Downloads\My Project Innov\lend-guard-ai-landing-page - Copy"
```

Execute schema creation:
```bash
# Using clickhouse-client
clickhouse-client --multiquery < warehouse/schema/dw_schema.sql
```

Or using Docker:
```bash
docker exec -i lendguard-warehouse clickhouse-client --multiquery < warehouse/schema/dw_schema.sql
```

Verify schema:
```bash
clickhouse-client --query "SHOW DATABASES"
# Should show: bronze_layer, silver_layer, gold_layer
```

---

## Step 3: Setup Python ETL Environment

Create virtual environment:
```bash
cd warehouse
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
```

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## Step 4: Configure Environment Variables

Add to your `.env` file:
```env
# Existing PostgreSQL (don't change)
DATABASE_URL="postgresql://user:pass@localhost:5432/lendguard"

# New ClickHouse connection
CLICKHOUSE_HOST=localhost
CLICKHOUSE_PORT=9000
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=
CLICKHOUSE_DATABASE=bronze_layer
```

---

## Step 5: Run Initial ETL Pipeline

Test the pipeline:
```bash
cd warehouse
python etl/pipeline.py
```

Expected output:
```
2024-01-15 10:30:00 - INFO - ✅ Database connections established
2024-01-15 10:30:01 - INFO - 🔍 Extracting loans from last 24 hours
2024-01-15 10:30:02 - INFO - 📦 Extracted 247 loan records
2024-01-15 10:30:02 - INFO - ✅ Bronze layer: Inserted 247 records
2024-01-15 10:30:03 - INFO - 🔄 Transforming Bronze → Silver
2024-01-15 10:30:03 - INFO - 📊 Processing 247 Bronze records
2024-01-15 10:30:04 - INFO - ✅ Silver layer: Transformed 247 records
2024-01-15 10:30:05 - INFO - 📈 Aggregating portfolio risk metrics
2024-01-15 10:30:05 - INFO - ✅ Gold layer: Portfolio risk aggregated
2024-01-15 10:30:06 - INFO - 🧠 Computing t-SNE dimension reduction (100D → 3D)
2024-01-15 10:30:06 - INFO - 🔬 Running t-SNE algorithm (this may take 30-60 seconds)...
2024-01-15 10:30:51 - INFO - ✅ t-SNE clusters: 247 users mapped to 3D space
2024-01-15 10:30:51 - INFO - ✅ Pipeline completed in 51.23 seconds
```

---

## Step 6: Verify Data in Warehouse

Query Bronze layer:
```bash
clickhouse-client --query "SELECT count() FROM bronze_layer.raw_loan_applications"
```

Query Silver layer:
```bash
clickhouse-client --query "SELECT risk_category, count() as cnt FROM silver_layer.clean_loan_applications GROUP BY risk_category"
```

Expected result:
```
┌─risk_category─┬─cnt─┐
│ LOW          │  82 │
│ MEDIUM       │ 115 │
│ HIGH         │  38 │
│ CRITICAL     │  12 │
└──────────────┴─────┘
```

Query Gold layer (t-SNE clusters):
```bash
clickhouse-client --query "SELECT cluster_id, count() as users, avg(default_probability) as avg_risk FROM gold_layer.user_risk_clusters GROUP BY cluster_id"
```

---

## Step 7: Schedule ETL Pipeline (Production)

### Windows Task Scheduler:
```powershell
# Create daily ETL task at 2 AM
$action = New-ScheduledTaskAction -Execute 'python' -Argument 'C:\Users\PC\Downloads\My Project Innov\lend-guard-ai-landing-page - Copy\warehouse\etl\pipeline.py'
$trigger = New-ScheduledTaskTrigger -Daily -At 2am
Register-ScheduledTask -TaskName "LendGuard-ETL" -Action $action -Trigger $trigger
```

### Alternative: Node.js Cron (using `node-cron`):
```typescript
// server/jobs/etl-scheduler.ts
import cron from 'node-cron';
import { exec } from 'child_process';

cron.schedule('0 2 * * *', () => {
  console.log('🚀 Running ETL pipeline...');
  exec('python warehouse/etl/pipeline.py', (error, stdout, stderr) => {
    if (error) {
      console.error(`❌ ETL failed: ${error.message}`);
      return;
    }
    console.log(stdout);
  });
});
```

---

## Step 8: Next Steps (Phase 2: Neural Networks)

1. ✅ Data Warehouse Foundation (COMPLETE)
2. ⬜ Train LSTM model on historical loan performance
3. ⬜ Implement Bayesian inference module
4. ⬜ Build 3D visualization dashboard (Three.js)

---

## Troubleshooting

**Error: ClickHouse connection refused**
```bash
# Check if ClickHouse is running
docker ps | grep clickhouse
# Restart if needed
docker restart lendguard-warehouse
```

**Error: psycopg2 connection failed**
```bash
# Verify PostgreSQL is running
# Check DATABASE_URL in .env
```

**Error: ModuleNotFoundError**
```bash
# Ensure virtual environment is activated
cd warehouse
.venv\Scripts\activate
pip install -r requirements.txt
```

**Performance: t-SNE taking too long**
```python
# In pipeline.py, reduce perplexity for smaller datasets:
tsne = TSNE(n_components=3, perplexity=15, n_iter=500)
```

---

## Performance Benchmarks

**Expected Processing Times:**
- Bronze extraction (1000 records): ~2 seconds
- Silver transformation: ~3 seconds
- Gold aggregation: ~1 second
- t-SNE dimension reduction (1000 users): ~45 seconds
- **Total ETL runtime:** ~51 seconds for 1000 records

**Query Performance:**
- Bronze raw query: ~100ms
- Silver analytical query: ~20ms
- Gold aggregated query: ~5ms (200x faster than OLTP)

---

## Success Criteria

✅ ClickHouse server running on port 9000  
✅ All 3 databases created (bronze/silver/gold)  
✅ ETL pipeline executes without errors  
✅ t-SNE produces 3D coordinates for visualization  
✅ Gold layer contains aggregated portfolio metrics  

**You are now ready for Phase 2: Neural Network Implementation**
