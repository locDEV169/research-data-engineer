-- Template MERGE Bronze (idempotent).
-- Script 02_load_bronze.py generate câu này cho từng bảng:
-- 1) load data vào {table}_staging (WRITE_TRUNCATE)
-- 2) MERGE vào bảng đích theo primary key
-- 3) xoá staging
--
-- Ví dụ cho customers:

MERGE `{project}.{bronze_dataset}.customers` AS target
USING `{project}.{bronze_dataset}.customers_staging` AS source
ON target.customer_id = source.customer_id
WHEN MATCHED THEN
  UPDATE SET
    customer_code = source.customer_code,
    full_name = source.full_name,
    date_of_birth = source.date_of_birth,
    gender = source.gender,
    phone_number = source.phone_number,
    email = source.email,
    city = source.city,
    customer_segment = source.customer_segment,
    kyc_status = source.kyc_status,
    created_at = source.created_at,
    updated_at = source.updated_at
WHEN NOT MATCHED THEN
  INSERT (
    customer_id, customer_code, full_name, date_of_birth, gender,
    phone_number, email, city, customer_segment, kyc_status,
    created_at, updated_at
  )
  VALUES (
    source.customer_id, source.customer_code, source.full_name, source.date_of_birth, source.gender,
    source.phone_number, source.email, source.city, source.customer_segment, source.kyc_status,
    source.created_at, source.updated_at
  );
