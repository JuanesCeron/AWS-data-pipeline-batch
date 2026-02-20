import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, count
from datetime import datetime

BUCKET = "data-pipeline-batch-juan-ceron"

if len(sys.argv) != 2:
    raise ValueError("Debes pasar execution_date como argumento: YYYY-MM-DD")

execution_date = sys.argv[1]

try:
    datetime.strptime(execution_date, "%Y-%m-%d")
except ValueError:
    raise ValueError("Formato inválido. Usa YYYY-MM-DD")

spark = (
    SparkSession.builder
    .appName("ExoplanetsGoldDashboard")
    .config("spark.hadoop.fs.s3a.aws.credentials.provider",
            "com.amazonaws.auth.DefaultAWSCredentialsProviderChain")
    .getOrCreate()
)

silver_path = f"s3a://{BUCKET}/silver/exoplanets/"
gold_base_path = f"s3a://{BUCKET}/gold/"

df = spark.read.parquet(silver_path)

# KPIs

kpis = df.agg(
    count("pl_name").alias("total_planets"),
    avg("pl_rade").alias("avg_radius"),
    avg("pl_bmasse").alias("avg_mass"),
    count("hostname").alias("total_records")
)

kpis.write.mode("overwrite").parquet(
    f"{gold_base_path}kpis/execution_date={execution_date}/"
)

# Planets per star

planets_by_star = (
    df.groupBy("hostname")
      .agg(
          count("pl_name").alias("planet_count"),
          avg("pl_rade").alias("avg_radius"),
          avg("pl_bmasse").alias("avg_mass")
      )
)

planets_by_star.write.mode("overwrite").parquet(
    f"{gold_base_path}planets_by_star/execution_date={execution_date}/"
)

# Ranking of worlds

planet_ranking = df.select(
    "pl_name",
    "hostname",
    "pl_rade",
    "pl_bmasse"
)

planet_ranking.write.mode("overwrite").parquet(
    f"{gold_base_path}planet_ranking/execution_date={execution_date}/"
)

spark.stop()
