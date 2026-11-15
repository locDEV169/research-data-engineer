"""Chay lan luot tung file .sql trong tests/manual_sql/ len BigQuery.

Day la cong cu thao tac/debug thu cong, KHONG phai pytest.

Cach chay:
    python scripts/run_manual_sql.py
"""

from etl.clients import connect_bigquery
from etl.settings import PROJECT_ROOT, load_config

SQL_DIR = PROJECT_ROOT / "tests" / "manual_sql"


def main():
    config = load_config()
    client = connect_bigquery(config)

    for sql_file in sorted(SQL_DIR.glob("*.sql")):
        print(f"Running {sql_file.name} ...")
        sql = sql_file.read_text(encoding="utf-8")
        client.query(sql).result()
        print(f"  done: {sql_file.name}")

    print("All SQL files executed successfully.")


if __name__ == "__main__":
    main()
