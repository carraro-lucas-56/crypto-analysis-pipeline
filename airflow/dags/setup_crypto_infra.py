from datetime import datetime

from airflow.sdk import DAG
from airflow.providers.google.cloud.operators.gcs import GCSCreateBucketOperator
from airflow.providers.google.cloud.operators.bigquery import (BigQueryCreateEmptyDatasetOperator,
                                                               BigQueryCreateTableOperator) 

from src.configs import BUCKET_NAME, CRYPTO_BUCKET_CONFIG, PROJECT_ID, BRONZE_MARKET_DATA_TABLE_CONFIG

with DAG(
    dag_id="setup_crypto_infra",
    start_date=datetime(2026,1,1),
    schedule=None,
    catchup=False
) as dag:

    create_bucket = GCSCreateBucketOperator(
        task_id="create_bucket",
        bucket_name=BUCKET_NAME,
        resource=CRYPTO_BUCKET_CONFIG,
        storage_class="STANDARD",

        retries=1,
        retry_delay=15
    ) 
    
    create_bronze_dataset = BigQueryCreateEmptyDatasetOperator(
        dataset_id="bronze",
        project_id=PROJECT_ID,
        dataset_reference={
            "description" : "Dataset to store the tables from the bronze layer"
        },
        location="US",
        task_id="create_bronze_dateset"
    )
    
    create_silver_dataset = BigQueryCreateEmptyDatasetOperator(
        dataset_id="silver",
        project_id=PROJECT_ID,
        dataset_reference={
            "description" : "Dataset to store the tables from the silver layer"
        },
        location="US",
        task_id="create_silver_dateset"
    )
    
    create_gold_dataset = BigQueryCreateEmptyDatasetOperator(
        dataset_id="gold",
        project_id=PROJECT_ID,
        dataset_reference={
            "description" : "Dataset to store the tables from the gold layer"
        },
        location="US",
        task_id="create_gold_dateset"
    )

    create_bronze_market_date_table = BigQueryCreateTableOperator(
        project_id=PROJECT_ID,
        table_resource=BRONZE_MARKET_DATA_TABLE_CONFIG,
        dataset_id="bronze",
        table_id="market_data",

        location="US",
        task_id="create_bronze_market_data_table"
    )

    # TASK STREAM

    (create_bucket >> create_bronze_dataset >> create_silver_dataset >> 
    create_gold_dataset >> create_bronze_market_date_table)

