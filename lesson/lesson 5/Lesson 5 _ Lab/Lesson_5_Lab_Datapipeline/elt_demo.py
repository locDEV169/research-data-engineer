"""elt_demo.py — biến thể ELT: nạp RAW trước, transform bằng SQL trong BigQuery.

Đây là phần DEMO ở slide (không lab). Đối chiếu với ETL trong main.py:
  - ETL: transform bằng pandas rồi mới load.
  - ELT: load raw lên kho trước, để BigQuery gánh transform bằng SQL.
"""
from google.cloud import bigquery

from etl.extract import extract_csv

RAW_TABLE = "myproj.raw.weather"          # bảng raw
MART_TABLE = "myproj.mart.weather"        # bảng đã transform


def run_elt():
    client = bigquery.Client()

    # 1) Nạp RAW thẳng lên kho (chưa làm sạch)
    df_raw = extract_csv("data/weather.csv")
    job = client.load_table_from_dataframe(df_raw, RAW_TABLE)
    job.result()

    # 2) Transform BẰNG SQL trong BigQuery
    sql = f"""
        CREATE OR REPLACE TABLE {MART_TABLE} AS
        SELECT INITCAP(TRIM(city)) AS city, temp_c
        FROM {RAW_TABLE}
        WHERE city IS NOT NULL
    """
    client.query(sql).result()
    print(f"[elt] Đã tạo {MART_TABLE} từ {RAW_TABLE} bằng SQL")


if __name__ == "__main__":
    run_elt()
