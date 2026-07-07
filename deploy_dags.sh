#!/usr/bin/env bash

set -euo pipefail

# Change this
COMPOSER_BUCKET=""

# Local source directory
DAGS_DIR="airflow/dags"

echo "Syncing DAGs to Composer..."

gsutil -m rsync \
    -r \
    -x '(^|/)(__pycache__)(/|$)|\.pyc$' \
    "${DAGS_DIR}" \
    "${COMPOSER_BUCKET}/dags"

echo "Done."

