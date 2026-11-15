from etl.clients import connect_bigquery, connect_postgres
from etl.settings import load_config


def main():
    config = load_config()

    print("Checking PostgreSQL source connection...")
    with connect_postgres(config) as conn:
        row = conn.execute("SELECT count(*) AS total_transactions FROM transactions").fetchone()
        print(f"PostgreSQL OK. transactions={row['total_transactions']}")

    print("Checking BigQuery connection...")
    client = connect_bigquery(config)
    rows = list(client.query("SELECT 1 AS ok").result())
    print(f"BigQuery OK. project={config['bigquery']['project_id']} result={rows[0]['ok']}")


if __name__ == "__main__":
    main()
