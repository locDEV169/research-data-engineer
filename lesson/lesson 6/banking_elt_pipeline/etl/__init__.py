"""ETL package cho pipeline PostgreSQL (core banking) -> BigQuery.

Mỗi module có đúng một trách nhiệm:
- settings: đọc .env, build config dict, PROJECT_ROOT.
- tables: khai báo source tables + metadata columns.
- clients: kết nối Postgres/BigQuery, helper đặt tên bảng, chạy file .sql.
- schema: build BigQuery schema cho bảng raw.
- watermark: đọc/ghi watermark theo từng source table.
- hashing: chuẩn hoá giá trị JSON + hash record.
- extract / load / transform / checks: 4 bước pipeline, mỗi module có run().
"""
