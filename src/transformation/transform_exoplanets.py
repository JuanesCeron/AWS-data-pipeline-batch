from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from datetime import datetime
import sys

BUCKET = "data-pipeline-batch-juan-ceron"

if len(sys.argv) != 2:
    raise ValueError("Debes pasar execution_date como argumento: YYYY-MM-DD")

execution_date = sys.argv[1]

try:
    datetime.strptime(execution_date, "%Y-%m-%d")
except ValueError:
    raise ValueError("Formato inválido. Usa YYYY-MM-DD")

bronze_path = f"s3a://{BUCKET}/bronze/exoplanets/{execution_date}/"
silver_path = f"s3a://{BUCKET}/silver/exoplanets/"

spark = (
    SparkSession.builder
    .appName("ExoplanetsTransformation")
    .config("spark.hadoop.fs.s3a.aws.credentials.provider",
            "com.amazonaws.auth.DefaultAWSCredentialsProviderChain")
    .getOrCreate()
)

df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(bronze_path)
)

df_clean = (
    df.select("pl_name", "hostname", "pl_orbper", "pl_rade", "pl_bmasse")
      .filter(col("pl_name").isNotNull())
      .filter(col("pl_orbper").isNotNull())
)

(
    df_clean
    .write
    .mode("overwrite")
    .parquet(silver_path)
)

spark.stop()
