from pathlib import Path

from .utils import get_query_str_from_file

PROJECT_ID = "crypto-analysis-pipeline"

# --------------------------------------------------
# ---------------- PATH CONFIG ---------------------
# --------------------------------------------------

# src/configs.py
CURRENT_DIR = Path(__file__).resolve().parent

# airflow/
AIRFLOW_DIR = CURRENT_DIR.parent

SQL_DIR = AIRFLOW_DIR / "sql"

# -----------------------------------------
# -------------- BUCKET CONFIG ------------
# -----------------------------------------

BUCKET_NAME = "crypto-data-56"

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
        "name": "circulating_supply_usd",
        "type": "INTEGER",
        "mode": "NULLABLE"
    },
    {
        "name": "ath_usd",
        "type": "INTEGER",
        "mode": "NULLABLE"
    },
    {
        "name": "ath_change_percentage",
        "type": "FLOAT",
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
        "name": "circulating_supply_usd",
        "type": "INTEGER",
        "mode": "REQUIRED"
    },
    {
        "name": "ath_usd",
        "type": "INTEGER",
        "mode": "REQUIRED"
    },
    {
        "name": "ath_change_percentage",
        "type": "FLOAT",
        "mode": "REQUIRED"
    },
    {
        "name": "snapshot_ts",
        "type": "TIMESTAMP",
        "mode": "REQUIRED"
    }
    ]
}

MARKET_CHANGES_SCHEMA = {
    "fields": [
        {
            "name": "coin_id",
            "type": "STRING",
            "mode": "REQUIRED"
        },
        {
            "name": "market_cap_change_1h",
            "type": "FLOAT",
            "mode": "REQUIRED"
        },
        {
            "name": "market_cap_change_percentage_1h",
            "type": "FLOAT",
            "mode": "REQUIRED"
        },
        {
            "name": "price_change_1h",
            "type": "FLOAT",
            "mode": "REQUIRED"
        },
        {
            "name": "current_price_change_percentage_1h",
            "type": "FLOAT",
            "mode": "REQUIRED"
        },
        {
            "name": "rank_change_1h",
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

COIN_VOLATILITY_SCHEMA = {
    "fields": [
        {
            "name": "coin_id",
            "type": "STRING",
            "mode": "REQUIRED"
        },
        {
            "name": "market_cap_volatility_24h",
            "type": "FLOAT",
            "mode": "REQUIRED"
        },
        {
            "name": "num_of_observations",
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

MARKET_SHARE_SCHEMA = {
    "fields": [
        {
            "name": "coin_id",
            "type": "STRING",
            "mode": "REQUIRED"
        },
        {
            "name": "market_share",
            "type": "FLOAT",
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

MARKET_CHANGES_TABLE_CONFIG = {
    "time_partitioning" : {
        "type": "DAY",
        "field": "snapshot_ts",   
    },
    "schema" : MARKET_CHANGES_SCHEMA
}

COIN_VOLATILITY_TABLE_CONFIG = {
    "time_partitioning" : {
        "type": "DAY",
        "field": "snapshot_ts",
    },
    "schema" : COIN_VOLATILITY_SCHEMA
}

MARKET_SHARE_TABLE_CONFIG = {
    "time_partitioning" : {
        "type": "DAY",
        "field": "snapshot_ts",
    },
    "schema" : MARKET_SHARE_SCHEMA
}

# ------------- QUERY STRINGS -------------

BRONZE_TO_SILVER_QUERY=get_query_str_from_file(SQL_DIR / "bronze_to_silver_query.sql")

MARKET_CHANGES_QUERY=get_query_str_from_file(SQL_DIR / "market_changes.sql")

COIN_VOLATILITY_QUERY=get_query_str_from_file(SQL_DIR / "coin_volatility.sql")

MARKET_SHARE_QUERY=get_query_str_from_file(SQL_DIR / "market_share.sql")

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

MARKET_CHANGES_JOG_CONFIG = {       
    "query": {
            "query": MARKET_CHANGES_QUERY,
            "useLegacySql": False,
        }
}

COIN_VOLATILITY_JOG_CONFIG = {
    "query": {
            "query": COIN_VOLATILITY_QUERY,
            "useLegacySql": False,
        }
}

MARKET_SHARE_JOG_CONFIG = {
    "query": {
            "query": MARKET_SHARE_QUERY,
            "useLegacySql": False,
        }
}

