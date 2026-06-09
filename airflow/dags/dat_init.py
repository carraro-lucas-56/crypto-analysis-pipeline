import os
import json
import tempfile
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv
from airflow.sdk import DAG, task, get_current_context
from airflow.exceptions import AirflowException
from airflow.providers.google.cloud.operators.gcs import GCSCreateBucketOperator
from airflow.providers.google.cloud.hooks.gcs import GCSHook

from src.extracy import CoinGeckoAPI
from src.transform import bronze_transform
from src.configs import CRYPTO_BUCKET_CONFIG, BUCKET_NAME

load_dotenv()

API_KEY = os.getenv("API_KEY")

with DAG(
    dag_id="crypto_dag",
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
        date_str = logical_date.strftime("%Y-%m-%d")                  

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

        object_name = f"bronze/{date_str}/hour{logical_date.hour:02d}.csv"
        transformed_data = bronze_transform(market_data,logical_date.isoformat())

        df = pd.DataFrame(transformed_data)

        with tempfile.NamedTemporaryFile(suffix=".csv") as f:
            df.to_csv(f.name, index=False)

            hook.upload(
                bucket_name=BUCKET_NAME,
                object_name=object_name,
                filename=f.name,
                mime_type="text/csv"
            )
    
        return object_name
    
    coins = fetch_top_coins_task()

    raw_object = fetch_and_upload_market_data(coins)

    bronze_object = bronze_transform_and_upload_task(raw_object)

    create_bucket >> coins 
