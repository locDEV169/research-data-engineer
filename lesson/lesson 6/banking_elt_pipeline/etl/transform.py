"""Buoc transform: chay MERGE SQL de bien raw thanh clean (dimension + fact)."""

from .clients import connect_bigquery, run_sql_file
from .settings import PROJECT_ROOT, load_config


def run():
    config = load_config()
    client = connect_bigquery(config)

    print("Running dimension MERGE SQL...")
    run_sql_file(
        client,
        config,
        PROJECT_ROOT / "sql" / "02_merge_dimensions.sql",
        {"hash_salt": config["hash_salt"].replace("'", "\\'")},
    )

    print("Running fact MERGE SQL...")
    run_sql_file(client, config, PROJECT_ROOT / "sql" / "03_merge_facts.sql")

    print("Clean transform complete.")


if __name__ == "__main__":
    run()
