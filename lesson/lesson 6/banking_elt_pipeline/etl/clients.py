from pathlib import Path

import psycopg
from google.cloud import bigquery
from psycopg.rows import dict_row


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
