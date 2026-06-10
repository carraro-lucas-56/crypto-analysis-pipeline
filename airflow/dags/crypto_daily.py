import os
import json
import tempfile
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv
from airflow.sdk import DAG, task, get_current_context
from airflow.exceptions import AirflowException
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator

from src.extracy import CoinGeckoAPI
from src.transform import bronze_transform
from src.configs import *

load_dotenv()

API_KEY = os.getenv("API_KEY")

with DAG(
    dag_id="crypto_dag",
    start_date=datetime(2026,1,1),
    schedule=None,
    catchup=False
) as dag:

    @task()
    def fetch_top_coins_task() -> list[str]:
        coin_gecko_client = CoinGeckoAPI(API_KEY)

        coins = coin_gecko_client.get_top_coins(10)
        
        if not coins:
            raise AirflowException()        

        return coins

    @task()
    def fetch_and_upload_market_data(coins: list[str]) -> str:
        
        # --------------------------------------
        # --- Fetching the data from the API ---
        # --------------------------------------

        coin_gecko_client = CoinGeckoAPI(API_KEY)

        market_data = coin_gecko_client.fetch_market_data(coins)

        if not market_data:
            raise AirflowException()

        # --------------------------------------
        # ---------- Uploading to GCS ----------
        # --------------------------------------
    
        context = get_current_context()

        hook = GCSHook(
            gcp_conn_id="google_cloud_default"
        )

        logical_date = context["logical_date"]
        date_str = logical_date.strftime("%Y-%m-%d")                  

        object_name = f"raw/{date_str}/hour{logical_date.hour:02d}.json"

        # Upload the file to GCS
        hook.upload(
            bucket_name=BUCKET_NAME,
            object_name=object_name,
            data=json.dumps(
                market_data,
                ensure_ascii=False,
            ),
            mime_type="application/json",
        )

        return object_name
        
    @task()
    def bronze_transform_and_upload_task(object_path: str) -> str:
    
        context = get_current_context()

        logical_date = context["logical_date"]

        hook = GCSHook(
            gcp_conn_id="google_cloud_default"
        )

        # --------------------------------------
        # ------- Downloading Raw Files --------
        # --------------------------------------

        raw_data = hook.download(
            bucket_name=BUCKET_NAME,
            object_name=object_path
        )

        market_data = json.loads(raw_data.decode("utf-8"))

        # --------------------------------------
        # - Uploading transformed data to GCS --
        # --------------------------------------

        object_name = (
            f"bronze/"
            f"year={logical_date.year}/"
            f"month={logical_date.month:02d}/"
            f"day={logical_date.day:02d}/"
            f"hour={logical_date.hour:02d}.parquet"
        )
        
        transformed_data = bronze_transform(market_data,logical_date)

        df = pd.DataFrame(transformed_data)
        df["snapshot_ts"] = pd.to_datetime(df["snapshot_ts"], utc=True)

        with tempfile.NamedTemporaryFile(suffix=".parquet") as f:
            df.to_parquet(f.name, 
                          index=False,
                          engine="pyarrow",
                          coerce_timestamps="us")

            hook.upload(
                bucket_name=BUCKET_NAME,
                object_name=object_name,
                filename=f.name,
                mime_type="application/octet-stream",
            )
    
        return object_name

    coins = fetch_top_coins_task()

    raw_object = fetch_and_upload_market_data(coins)

    bronze_object = bronze_transform_and_upload_task(raw_object)

    bronze_to_bq = BigQueryInsertJobOperator(
        task_id="load_bronze_to_bigquery",
        configuration=LOAD_TO_BQ_CONFIG(bronze_object),
        project_id=PROJECT_ID,
        location="US",
    )

    coins >> raw_object >> bronze_object >> bronze_to_bq
