from helper import PROJECT_ROOT, connect_bigquery, load_config, run_sql_file


def main():
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
    print("Next step: python 04_check_result.py")


if __name__ == "__main__":
    main()
