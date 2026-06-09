DATA_DIR="/home/lucas/crypto-analysis/Data"

PROJECT_ID="crypto-analysis-pipeline"

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

