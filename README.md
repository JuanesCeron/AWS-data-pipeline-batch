# 🚀 AWS Data Pipeline Batch – Exoplanets Lakehouse

End-to-end batch data pipeline built with Apache Spark and AWS, implementing a Bronze–Silver–Gold Lakehouse architecture.

This project ingests exoplanet data from a public API, processes it through multiple transformation layers, and makes it available for analytics using Amazon Athena and Power BI.

---

## 🏗️ Architecture
```bash
Data Source (API)
↓
Bronze Layer (Raw Data - S3)
↓
Silver Layer (Cleaned & Validated - S3)
↓
Gold Layer (Aggregated - S3)
↓
Amazon Athena
↓
Power BI Dashboard
```
### AWS Services Used

- Amazon S3 – Data Lake storage  
- Amazon Athena – SQL query engine over S3  
- Apache Spark – Distributed data processing  

---

## 📂 Project Structure
```bash
aws-data-pipeline-batch/
│
├── config/
│ └── config.yaml
│
├── src/
│ ├── ingestion/
│ │ └── fetch_exoplanets.py
│ │
│ ├── transformation/
│ │ └── transform_exoplanets.py
│ │
│ └── analytics/
│ └── dashboard_exoplanets.py
│
├── requirements.txt
├── setup.py
└── README.md
```

---

## Data Layers

### Bronze
- Raw data ingestion from API
- Stored in Parquet format
- Partitioned by `execution_date`

### Silver
- Data cleaning and validation
- Type casting
- Null handling
- Schema enforcement

### Gold
- Business-level aggregations
- Example:
  - Planets per star
  - Average radius
  - Average mass
- Optimized for analytics queries

---

## Configuration

All environment settings are handled through:
config/config.yaml

Example:

```yaml
aws:
  region: us-east-1
  bucket: exoplanets-lakehouse-bucket

paths:
  bronze: bronze/exoplanets/
  silver: silver/exoplanets/
  gold: gold/planets_by_star/
```
No credentials are stored in the repository.

---

## ▶️ How to Run

### 1️⃣ Install dependencies
```bash
pip install -r requirements.txt
```
### 2️⃣ Run Bronze Layer
```bash
spark-submit src/ingestion/fetch_exoplanets.py --execution_date 2026-02-23
```
### 3️⃣ Run Silver & Gold
```bash
spark-submit src/transformation/transform_exoplanets.py --execution_date 2026-02-23
```

---

## Querying with Athena

Once Gold data is available in S3:

```sql
SELECT *
FROM planets_by_star
WHERE execution_date = '2026-02-23'
LIMIT 10;
```

Athena scans Parquet files directly from S3.

---

## 📊 Dashboard

Gold layer is connected to Power BI using Amazon Athena as the data source.

Example insights:

- Stars with most exoplanets
- Average planetary mass by system
- Distribution of planetary radius

---

## Key Engineering Concepts Demonstrated

- Lakehouse architecture
- Partitioned Parquet storage
- External tables in Athena
- Metadata management
- Batch processing
- Configuration-driven pipelines
- Cloud-native data analytics

---

## Security

- No AWS credentials stored
- IAM-based authentication
- Data stored in S3 with partitioning strategy

---

## Future Improvements

- Infrastructure as Code (Terraform)
- CI/CD pipeline
- Data quality checks
- Airflow orchestration
- Glue Catalog integration

---

👤 Author

Juan Esteban Cerón – Data Engineering Portfolio Project

