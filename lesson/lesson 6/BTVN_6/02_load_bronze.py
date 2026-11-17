"""Extract Postgres → staging → MERGE vào Bronze (idempotent).

Cách chạy:
    python 02_load_bronze.py              # tất cả bảng
    python 02_load_bronze.py customers    # một bảng
"""

import sys

import pandas as pd  # pyright: ignore[reportMissingImports]
from config_tables import SOURCE_TABLES
from google.cloud import bigquery
from helper import (
    connect_bigquery,
    connect_postgres,
    load_config,
    quoted_table,
    table_id,
    table_schema,
)


def extract_rows(conn, table):
    columns = ", ".join(table["columns"].keys())
    sql = f"SELECT {columns} FROM {table['name']}"
    return list(conn.execute(sql).fetchall())


def to_dataframe(table, rows):
    return pd.DataFrame(rows, columns=list(table["columns"].keys()))


def load_staging(client, config, table, dataframe):
    dataset = config["bigquery"]["bronze_dataset"]
    staging_name = f"{table['name']}_staging"
    destination = table_id(config, dataset, staging_name)
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        schema=table_schema(table),
    )
    client.load_table_from_dataframe(
        dataframe, destination, job_config=job_config
    ).result()
    return staging_name


def build_merge_sql(config, table, staging_name):
    dataset = config["bigquery"]["bronze_dataset"]
    target = quoted_table(config, dataset, table["name"])
    source = quoted_table(config, dataset, staging_name)
    pk = table["primary_key"]
    columns = list(table["columns"].keys())
    non_pk = [c for c in columns if c != pk]

    update_set = ",\n    ".join(f"{c} = source.{c}" for c in non_pk)
    insert_cols = ", ".join(columns)
    insert_vals = ", ".join(f"source.{c}" for c in columns)

    return f"""
MERGE {target} AS target
USING {source} AS source
ON target.{pk} = source.{pk}
WHEN MATCHED THEN
  UPDATE SET
    {update_set}
WHEN NOT MATCHED THEN
  INSERT ({insert_cols})
  VALUES ({insert_vals})
"""


def drop_staging(client, config, staging_name):
    dataset = config["bigquery"]["bronze_dataset"]
    client.delete_table(table_id(config, dataset, staging_name), not_found_ok=True)


def load_table(client, source_conn, config, table):
    rows = extract_rows(source_conn, table)
    df = to_dataframe(table, rows)
    if df.empty:
        print(f"  {table['name']}: 0 rows (skip merge)")
        return 0

    staging_name = load_staging(client, config, table, df)
    merge_sql = build_merge_sql(config, table, staging_name)
    client.query(merge_sql).result()
    drop_staging(client, config, staging_name)
    print(f"  {table['name']}: merged {len(rows)} rows")
    return len(rows)


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    tables = SOURCE_TABLES
    if only:
        tables = [t for t in SOURCE_TABLES if t["name"] == only]
        if not tables:
            raise SystemExit(f"Unknown table: {only}")

    config = load_config()
    client = connect_bigquery(config)

    print(f"Loading bronze dataset={config['bigquery']['bronze_dataset']}")
    with connect_postgres(config) as source_conn:
        for table in tables:
            load_table(client, source_conn, config, table)

    print("Bronze load complete.")


if __name__ == "__main__":
    main()
