from google.cloud import bigquery

from .clients import quoted_table


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
