# """Chạy lần lượt từng file .sql trong folder test_sql/ lên BigQuery.

# Cách chạy:
#     python run_test_sql.py
# """

# from pathlib import Path

# from helper import connect_bigquery, load_config

# SQL_DIR = Path(__file__).resolve().parent / "test_sql"

# config = load_config()
# client = connect_bigquery(config)

# for sql_file in sorted(SQL_DIR.glob("*.sql")):
#     print(f"Running {sql_file.name} ...")
#     sql = sql_file.read_text(encoding="utf-8")
#     client.query(sql).result()
#     print(f"  done: {sql_file.name}")

# print("All SQL files executed successfully.")




import os
from google.cloud import bigquery
from helper import load_config, connect_bigquery
from pathlib import Path

config = load_config()
client = connect_bigquery(config)
sql_path = Path(__file__).resolve().parent / 'test_sql'

def run_bigquery_from_file():
    for sql_file_path in sql_path.glob("*.sql"):
        with open(sql_file_path, "r", encoding="utf-8") as file:
            query_string = file.read()

        print("Submitting query from file to BigQuery engine...")

        query_job = client.query(query_string)  
        results = query_job.to_dataframe()           

    return results


if __name__ == "__main__":
    results = run_bigquery_from_file()
    print(results)
