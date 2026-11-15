import pandas as pd
from google.cloud import bigquery

from .clients import connect_bigquery, connect_postgres, table_id
from .schema import raw_schema
from .settings import load_config
from .tables import SOURCE_TABLES
from .watermark import get_watermark, set_watermark


def build_extract_query(table, last_watermark):
    columns = ", ".join(table["columns"].keys())
    watermark = table["watermark"]

    if last_watermark is None:
        return f"SELECT {columns} FROM {table['name']} ORDER BY {watermark}"

    return f"SELECT {columns} FROM {table['name']} WHERE {watermark} > '{last_watermark}' ORDER BY {watermark}"


def to_dataframe(table, rows):
    column_names = list(table["columns"].keys())
    return pd.DataFrame(rows, columns=column_names)


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


def run():
    config = load_config()
    client = connect_bigquery(config)

    print("Starting raw load.")

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


if __name__ == "__main__":
    run()
