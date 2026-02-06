# AWS Batch Data Pipeline

This project implements a production-style batch data pipeline on AWS using
S3 as a data lake (bronze/silver/gold architecture) and Airflow for orchestration.

## Status
- AWS account and CLI configured
- S3 bucket created
- Data lake structure initialized (bronze/silver/gold)

## Architecture (planned)
- Ingestion → S3 Bronze
- Processing → Silver
- Analytics → Gold
