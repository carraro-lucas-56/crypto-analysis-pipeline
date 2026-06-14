from .utils import get_query_str_from_file

DATA_DIR="/home/lucas/crypto-analysis/Data"

PROJECT_ID="crypto-analysis-pipeline"

SQL_DIR="/home/lucas/crypto-analysis/airflow/sql"

# -----------------------------------------
# ------------ BUCKET CONFIGS -------------
# -----------------------------------------

BUCKET_NAME="crypto-data-56"

CRYPTO_BUCKET_CONFIG = {
            "lifecycle" : {
                "rule" : [
                    {
                        "action" : {"type" : "SetStorageClass",
                                    "storageClass" : "NEARLINE"},
                        "condition" : {"age" : 30}
                    }
                ]
            },

            "versioning" : {
                "enable" : True
            },

            "iamConfiguration": {
                "uniformBucketLevelAccess": {
                    "enabled": True
                }
            }
        }

# -----------------------------------------
# ----------- BIGQUERY CONFIGS ------------
# -----------------------------------------

# --------------- SCHEMAS -----------------

BRONZE_MARKET_DATA_SCHEMA = { 
    "fields" : [
    {
        "name": "coin_id",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "symbol",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "name",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "current_price_usd",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "market_cap_usd",
        "type": "INTEGER",
        "mode": "NULLABLE"
    },
    {
        "name": "market_cap_rank",
        "type": "INTEGER",
        "mode": "NULLABLE"
    },
    {
        "name": "total_volume_usd",
        "type": "INTEGER",
        "mode": "NULLABLE"
    },
    {
        "name": "snapshot_ts",
        "type": "TIMESTAMP",
        "mode": "NULLABLE"
    }
    ]
}

SILVER_MARKET_DATA_SCHEMA = { 
    "fields" : [
    {
        "name": "coin_id",
        "type": "STRING",
        "mode": "REQUIRED"
    },
    {
        "name": "symbol",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "name",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "current_price_usd",
        "type": "FLOAT",
        "mode": "REQUIRED"
    },
    {
        "name": "market_cap_usd",
        "type": "INTEGER",
        "mode": "REQUIRED"
    },
    {
        "name": "market_cap_rank",
        "type": "INTEGER",
        "mode": "REQUIRED"
    },
    {
        "name": "total_volume_usd",
        "type": "INTEGER",
        "mode": "REQUIRED"
    },
    {
        "name": "snapshot_ts",
        "type": "TIMESTAMP",
        "mode": "REQUIRED"
    }
    ]
}

# ------------- TABLE CONFIGS -------------

BRONZE_MARKET_DATA_TABLE_CONFIG = {
    "time_partitioning" : {
        "type": "DAY",
        "field": "snapshot_ts",   
    },
    "schema" : BRONZE_MARKET_DATA_SCHEMA
}

SILVER_MARKET_DATA_TABLE_CONFIG = {
    "time_partitioning" : {
        "type": "DAY",
        "field": "snapshot_ts",   
    },
    "schema" : SILVER_MARKET_DATA_SCHEMA
}

# ------------- QUERY STRINGS -------------

BRONZE_TO_SILVER_QUERY=get_query_str_from_file(f"{SQL_DIR}/bronze_to_silver_query.sql")     

# ------------- JOB CONFIGS ---------------

def LOAD_TO_BQ_CONFIG(object_name: str) -> dict: 
    return {    
        "load": {
            "sourceUris": [f"gs://{BUCKET_NAME}/{object_name}"],
            "destinationTable": {
                "projectId": PROJECT_ID,
                "datasetId": "bronze",
                "tableId": "market_data",
            },
            "sourceFormat": "PARQUET",
            "writeDisposition": "WRITE_APPEND",
            "schema" : BRONZE_MARKET_DATA_SCHEMA
        }
    }

BRONZE_TO_SILVER_JOB_CONFIG = {       
    "query": {
            "query": BRONZE_TO_SILVER_QUERY,
            "useLegacySql": False,
        }
}
