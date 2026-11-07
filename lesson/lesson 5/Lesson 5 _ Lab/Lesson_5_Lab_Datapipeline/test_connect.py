"""test_connect.py — kiểm tra môi trường đã kết nối BigQuery chưa (phần pre-work).

Chạy được và in ra ok = 1 nghĩa là môi trường sẵn sàng.
"""
from google.cloud import bigquery

# Client tự đọc biến môi trường GOOGLE_APPLICATION_CREDENTIALS
client = bigquery.Client()

df = client.query("SELECT 1 AS ok").to_dataframe()
print(df)
