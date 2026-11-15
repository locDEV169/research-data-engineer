"""Buoc khoi tao: tao dataset/table BigQuery can dung (raw + clean + ops)."""

from .clients import connect_bigquery, create_dataset, run_sql_file
from .schema import create_raw_table
from .settings import PROJECT_ROOT, load_config
from .tables import SOURCE_TABLES
from .watermark import create_watermark_table


def run():
    config = load_config()
    client = connect_bigquery(config)
    bq = config["bigquery"]

    print("Creating BigQuery datasets...")
    create_dataset(client, config, bq["raw_dataset"])
    create_dataset(client, config, bq["clean_dataset"])
    create_dataset(client, config, bq["ops_dataset"])

    print("Creating watermark table...")
    create_watermark_table(client, config)

    print("Creating raw tables...")
    for table in SOURCE_TABLES:
        create_raw_table(client, config, table)
        print(f"  ready: raw.{table['name']}")

    print("Creating clean tables...")
    run_sql_file(client, config, PROJECT_ROOT / "sql" / "01_create_clean_tables.sql")

    print("BigQuery initialization complete.")


if __name__ == "__main__":
    run()
