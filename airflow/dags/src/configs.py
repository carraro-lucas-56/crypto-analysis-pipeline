DATA_DIR="/home/lucas/crypto-analysis/Data"

PROJECT_ID="crypto-analysis-pipeline"

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
        "name": "current_price",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "market_cap",
        "type": "INTEGER",
        "mode": "NULLABLE"
    },
    {
        "name": "market_cap_rank",
        "type": "INTEGER",
        "mode": "NULLABLE"
    },
    {
        "name": "total_volume",
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

BRONZE_MARKET_DATA_TABLE_CONFIG = {
    "time_partitioning" : {
        "type": "DAY",
        "field": "snapshot_ts",   
    },
    "schema" : BRONZE_MARKET_DATA_SCHEMA
}

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
