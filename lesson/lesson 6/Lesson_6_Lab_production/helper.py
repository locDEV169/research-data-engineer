import hashlib
import json
import os
from datetime import UTC, date, datetime
from decimal import Decimal
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from google.cloud import bigquery
from psycopg.rows import dict_row

from config_tables import METADATA_COLUMNS


PROJECT_ROOT = Path(__file__).resolve().parent

def get_env(name, default=None):
    value = os.getenv(name, default)
    if value is None or value == "":
        raise ValueError(f"Missing environment variable: {name}")
    return value


def load_config():
    load_dotenv(PROJECT_ROOT / ".env")
    # get_env("GOOGLE_APPLICATION_CREDENTIALS")

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


def raw_schema(table):
    schema = []
    # all_columns = {**table["columns"], **METADATA_COLUMNS}
    all_columns = {**table["columns"]}
    for column_name, column_type in all_columns.items():
        schema.append(bigquery.SchemaField(column_name, column_type, mode="NULLABLE"))
    return schema


def create_raw_table(client, config, table):
    raw_dataset = config["bigquery"]["raw_dataset"]
    bq_table = bigquery.Table(table_id(config, raw_dataset, table["name"]), schema=raw_schema(table))
    client.create_table(bq_table, exists_ok=True)


def run_sql_file(client, config, sql_file, extra_values=None):
    extra_values = extra_values or {}
    bq = config["bigquery"]
    sql = Path(sql_file).read_text(encoding="utf-8").format(
        project=bq["project_id"],
        raw_dataset=bq["raw_dataset"],
        clean_dataset=bq["clean_dataset"],
        ops_dataset=bq["ops_dataset"],
        **extra_values,
    )
    return client.query(sql).result()


def create_watermark_table(client, config):
    ops_dataset = config["bigquery"]["ops_dataset"]
    client.query(
        f"""
        CREATE TABLE IF NOT EXISTS {quoted_table(config, ops_dataset, "watermarks")} (
          source_table STRING NOT NULL,
          last_watermark_value TIMESTAMP,
          updated_at TIMESTAMP NOT NULL
        )
        """
    ).result()


def get_watermark(client, config, source_table):
    ops_dataset = config["bigquery"]["ops_dataset"]
    rows = list(
        client.query(
            f"""
            SELECT last_watermark_value
            FROM {quoted_table(config, ops_dataset, "watermarks")}
            WHERE source_table = @source_table
            """,
            job_config=bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("source_table", "STRING", source_table),
                ]
            ),
        ).result()
    )
    return rows[0]["last_watermark_value"] if rows else None


def set_watermark(client, config, source_table, value):
    ops_dataset = config["bigquery"]["ops_dataset"]
    client.query(
        f"""
        MERGE {quoted_table(config, ops_dataset, "watermarks")} AS target
        USING (SELECT @source_table AS source_table, @value AS last_watermark_value) AS source
        ON target.source_table = source.source_table
        WHEN MATCHED THEN
          UPDATE SET last_watermark_value = source.last_watermark_value,
                     updated_at = CURRENT_TIMESTAMP()
        WHEN NOT MATCHED THEN
          INSERT (source_table, last_watermark_value, updated_at)
          VALUES (source.source_table, source.last_watermark_value, CURRENT_TIMESTAMP())
        """,
        job_config=bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("source_table", "STRING", source_table),
                bigquery.ScalarQueryParameter("value", "TIMESTAMP", value),
            ]
        ),
    ).result()


def json_value(value):
    if isinstance(value, datetime):
        return value.astimezone(UTC).isoformat() if value.tzinfo else value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, Decimal):
        return str(value)
    return value


def json_rows(rows):
    return [{key: json_value(value) for key, value in row.items()} for row in rows]


def stable_record_hash(record, columns):
    data = {column: record.get(column) for column in columns}
    text = json.dumps(data, sort_keys=True, default=str, separators=(",", ":"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
