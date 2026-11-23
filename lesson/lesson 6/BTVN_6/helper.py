import os
from pathlib import Path

import psycopg  # pyright: ignore[reportMissingImports]
from dotenv import load_dotenv  # pyright: ignore[reportMissingImports]
from google.cloud import bigquery  # pyright: ignore[reportMissingImports]
from psycopg.rows import dict_row  # pyright: ignore[reportMissingImports]

PROJECT_ROOT = Path(__file__).resolve().parent


def get_env(name, default=None):
    value = os.getenv(name, default)
    if value is None or value == "":
        raise ValueError(f"Missing environment variable: {name}")
    return value


def _resolve_credentials_path(cred: str) -> Path | None:
    """Resolve SA key path: absolute, cwd, or relative to project/repo roots."""
    raw = Path(cred).expanduser()
    candidates = [raw]
    if not raw.is_absolute():
        candidates.extend(
            [
                PROJECT_ROOT / raw,
                PROJECT_ROOT.parent / raw,  # ../private_key from BTVN_6
                PROJECT_ROOT.parents[2] / raw,  # repo root relative
                PROJECT_ROOT.parents[3] / raw.name if raw.name else raw,  # sibling folder
            ]
        )
        # Common layout: <parent>/private_key/<file> next to research-data-engineer/
        candidates.append(PROJECT_ROOT.parents[3] / "private_key" / raw.name)
        candidates.append(PROJECT_ROOT.parents[2].parent / "private_key" / raw.name)
    for path in candidates:
        try:
            resolved = path.resolve()
        except OSError:
            continue
        if resolved.exists():
            return resolved
    return None


def _prepare_gcp_credentials():
    """Resolve SA key path; if missing, fall back to ADC."""
    cred = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
    if not cred:
        return
    resolved = _resolve_credentials_path(cred)
    if resolved is None:
        print(f"WARN: SA key not found: {cred}")
        print("Falling back to Application Default Credentials (gcloud auth).")
        os.environ.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
        return
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(resolved)


def load_config():
    load_dotenv(PROJECT_ROOT / ".env")
    _prepare_gcp_credentials()

    return {
        "pipeline_name": get_env("PIPELINE_NAME", "banking_bronze_elt"),
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
            "bronze_dataset": get_env("BQ_BRONZE_DATASET", "banking_bronze"),
        },
        "source_system": get_env("SOURCE_SYSTEM", "CORE_BANKING"),
    }


def connect_postgres(config):
    db = config["source_db"]
    dsn = (
        f"host={db['host']} port={db['port']} dbname={db['database']} "
        f"user={db['user']} password={db['password']} connect_timeout=15"
    )
    return psycopg.connect(dsn, row_factory=dict_row)


def connect_bigquery(config):
    bq = config["bigquery"]
    return bigquery.Client(project=bq["project_id"], location=bq["location"])


def table_id(config, dataset_name, table_name):
    return f"{config['bigquery']['project_id']}.{dataset_name}.{table_name}"


def quoted_table(config, dataset_name, table_name):
    return f"`{table_id(config, dataset_name, table_name)}`"


def create_dataset(client, config, dataset_name):
    dataset = bigquery.Dataset(f"{config['bigquery']['project_id']}.{dataset_name}")
    dataset.location = config["bigquery"]["location"]
    client.create_dataset(dataset, exists_ok=True)


def table_schema(table):
    return [
        bigquery.SchemaField(name, bq_type, mode="NULLABLE")
        for name, bq_type in table["columns"].items()
    ]


def create_bronze_table(client, config, table):
    dataset = config["bigquery"]["bronze_dataset"]
    bq_table = bigquery.Table(
        table_id(config, dataset, table["name"]),
        schema=table_schema(table),
    )
    client.create_table(bq_table, exists_ok=True)


def run_sql_file(client, config, sql_file, extra_values=None):
    extra_values = extra_values or {}
    bq = config["bigquery"]
    sql = (
        Path(sql_file)
        .read_text(encoding="utf-8")
        .format(
            project=bq["project_id"],
            bronze_dataset=bq["bronze_dataset"],
            **extra_values,
        )
    )
    return client.query(sql).result()
