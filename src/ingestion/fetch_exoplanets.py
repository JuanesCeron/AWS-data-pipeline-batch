import requests
import boto3
from datetime import datetime

# Configuration

NASA_EXOPLANET_CSV_URL = (
    "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?"
    "query=select+*+from+pscomppars&format=csv"
)

S3_BUCKET = "data-pipeline-batch-juan-ceron"
S3_PREFIX = "bronze/exoplanets"


# Data Ingestion Function

def fetch_and_upload_exoplanets():
    print("Fetching exoplanet data from NASA...")

    response = requests.get(NASA_EXOPLANET_CSV_URL)
    response.raise_for_status()

    csv_data = response.text
    print("Data fetched successfully.")

    # Timestamp para versionado
    execution_date = datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    s3_key = f"{S3_PREFIX}/{execution_date}/exoplanets.csv"

    # Cliente S3
    s3_client = boto3.client("s3")

    # Subir a S3
    s3_client.put_object(
        Bucket=S3_BUCKET,
        Key=s3_key,
        Body=csv_data
    )

    print(f"Data uploaded to s3://{S3_BUCKET}/{s3_key}")

if __name__ == "__main__":
    fetch_and_upload_exoplanets()
