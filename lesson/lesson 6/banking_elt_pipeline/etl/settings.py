import os
from pathlib import Path

from dotenv import load_dotenv

# etl/settings.py -> parent la etl/, parent.parent la root cua project
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def get_env(name, default=None):
    value = os.getenv(name, default)
    if value is None or value == "":
        raise ValueError(f"Missing environment variable: {name}")
    return value


def load_config():
    load_dotenv(PROJECT_ROOT / ".env")

    return {
        "pipeline_name": get_env("PIPELINE_NAME", "banking_bigquery_elt"),
        "source_db": {
            "host": get_env("SOURCE_DB_HOST"),
            "port": int(get_env("SOURCE_DB_PORT", "15432")),
            "database": get_env("SOURCE_DB_NAME", "core_banking"),
            "user": get_env("SOURCE_DB_USER", "de_source_exporter"),
            "password": get_env("SOURCE_DB_PASSWORD"),
        },
        "bigquery": {
            "project_id": get_env("BQ_PROJECT_ID"),
            "location": get_env("BQ_LOCATION", "asia-southeast1"),
            "raw_dataset": get_env("BQ_RAW_DATASET", "banking_raw"),
            "clean_dataset": get_env("BQ_CLEAN_DATASET", "banking_clean"),
            "ops_dataset": get_env("BQ_OPS_DATASET", "banking_ops"),
        },
        "hash_salt": get_env("HASH_SALT"),
        "source_system": get_env("SOURCE_SYSTEM", "CORE_BANKING"),
    }
