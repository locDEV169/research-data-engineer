"""Bước LOAD — nạp DataFrame lên BigQuery.

table_id gồm 3 phần: "project.dataset.table".
"""
from google.cloud import bigquery


def load(df, table_id: str, write_disposition: str = "WRITE_APPEND"):
    """Nạp DataFrame lên một bảng BigQuery.

    write_disposition:
      - WRITE_APPEND   : nối thêm (mặc định) → CHẠY LẠI SẼ NHÂN ĐÔI dữ liệu.
      - WRITE_TRUNCATE : xoá sạch rồi ghi lại (full load, tránh trùng).
    Cơ chế incremental chống trùng đúng cách (watermark + MERGE) sẽ học ở BUỔI 4.
    """
    client = bigquery.Client()
    job_config = bigquery.LoadJobConfig(write_disposition=write_disposition)
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()  # chặn tới khi job nạp xong
    print(f"[load] Đã nạp {len(df)} dòng vào {table_id} ({write_disposition})")
