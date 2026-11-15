from google.cloud import bigquery

from .clients import table_id


def raw_schema(table):
    schema = []
    all_columns = {**table["columns"]}
    for column_name, column_type in all_columns.items():
        schema.append(bigquery.SchemaField(column_name, column_type, mode="NULLABLE"))
    return schema


def create_raw_table(client, config, table):
    raw_dataset = config["bigquery"]["raw_dataset"]
    bq_table = bigquery.Table(table_id(config, raw_dataset, table["name"]), schema=raw_schema(table))
    client.create_table(bq_table, exists_ok=True)
