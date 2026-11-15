import uuid
from datetime import UTC, datetime

import pandas as pd
from google.cloud import bigquery

from config_tables import SOURCE_TABLES
from helper import (
    connect_bigquery,
    connect_postgres,
    get_watermark,
    load_config,
    raw_schema,
    set_watermark,
    table_id,
)


def build_extract_query(table, last_watermark):
    columns = ", ".join(table["columns"].keys())
    watermark = table["watermark"]

    if last_watermark is None:
        return f"SELECT {columns} FROM {table['name']} ORDER BY {watermark}"

    sql = f"SELECT {columns} FROM {table['name']} WHERE {watermark} > '{last_watermark}' ORDER BY {watermark}"
    return sql


def to_dataframe(table, rows):
    columns = table["columns"]

    column_names = list(columns.keys())

    df = pd.DataFrame(
        rows,
        columns=column_names
    )

    return df


def load_to_bigquery_raw(client, config, table, dataframe):
    if dataframe.empty:
        return

    schema = raw_schema(table)
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        schema=schema,
    )
    load_job = client.load_table_from_dataframe(
        dataframe[[field.name for field in schema]],
        table_id(config, config["bigquery"]["raw_dataset"], table["name"]),
        job_config=job_config,
    )
    load_job.result()


def main():
    config = load_config()
    client = connect_bigquery(config)

    print(f"Starting raw load.")

    with connect_postgres(config) as source_conn:
        for table in SOURCE_TABLES:
            last_watermark = get_watermark(client, config, table["name"])
            sql = build_extract_query(table, last_watermark)
            rows = list(source_conn.execute(sql).fetchall())

            dataframe = to_dataframe(table, rows)
            load_to_bigquery_raw(client, config, table, dataframe)

            new_watermark = last_watermark
            if rows:
                new_watermark = rows[-1][table["watermark"]]
                set_watermark(client, config, table["name"], new_watermark)

            print(f"  raw.{table['name']}: {len(rows)} rows | watermark {last_watermark} -> {new_watermark}")

    print("Raw load complete.")
    print("Next step: python 03_transform_clean.py")


if __name__ == "__main__":
    main()
