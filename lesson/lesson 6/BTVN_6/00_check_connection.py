from helper import connect_bigquery, connect_postgres, load_config


def main():
    config = load_config()

    print("Checking PostgreSQL source...")
    with connect_postgres(config) as conn:
        row = conn.execute(
            "SELECT count(*) AS total_transactions FROM transactions"
        ).fetchone()
    print(f"PostgreSQL OK. transactions={row['total_transactions']}")

    print("Checking BigQuery...")
    try:
        client = connect_bigquery(config)
        rows = list(client.query("SELECT 1 AS ok").result())
    except Exception as exc:
        print("BigQuery FAILED.")
        print("Fix GOOGLE_APPLICATION_CREDENTIALS in .env to a local SA JSON that exists,")
        print("and ensure that SA can create jobs on BQ_PROJECT_ID.")
        raise SystemExit(f"BigQuery error: {exc}") from exc
    print(
        f"BigQuery OK. project={config['bigquery']['project_id']} "
        f"bronze={config['bigquery']['bronze_dataset']} result={rows[0]['ok']}"
    )


if __name__ == "__main__":
    main()
