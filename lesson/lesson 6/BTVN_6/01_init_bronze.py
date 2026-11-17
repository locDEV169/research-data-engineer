from config_tables import SOURCE_TABLES
from helper import (
    PROJECT_ROOT,
    connect_bigquery,
    create_dataset,
    load_config,
    run_sql_file,
)


def main():
    config = load_config()
    client = connect_bigquery(config)
    bronze = config["bigquery"]["bronze_dataset"]

    print(f"Creating dataset {bronze}...")
    create_dataset(client, config, bronze)

    print("Creating bronze tables from sql/01_create_bronze_tables.sql...")
    run_sql_file(client, config, PROJECT_ROOT / "sql" / "01_create_bronze_tables.sql")

    for table in SOURCE_TABLES:
        print(f"  ready: {bronze}.{table['name']}")

    print("Bronze init complete.")


if __name__ == "__main__":
    main()
