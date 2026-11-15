MERGE `{project}.{clean_dataset}.dim_date` target
USING (
  SELECT
    CAST(FORMAT_DATE('%Y%m%d', d) AS INT64) AS date_key,
    d AS full_date,
    EXTRACT(DAY FROM d) AS day_of_month,
    EXTRACT(MONTH FROM d) AS month_number,
    EXTRACT(QUARTER FROM d) AS quarter_number,
    EXTRACT(YEAR FROM d) AS year_number,
    FORMAT_DATE('%A', d) AS day_name
  FROM UNNEST(GENERATE_DATE_ARRAY(
    COALESCE((SELECT MIN(DATE(transaction_time)) FROM `{project}.{raw_dataset}.transactions` WHERE transaction_time IS NOT NULL), DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)),
    COALESCE((SELECT MAX(DATE(transaction_time)) FROM `{project}.{raw_dataset}.transactions` WHERE transaction_time IS NOT NULL), CURRENT_DATE())
  )) AS d
) source
ON target.date_key = source.date_key
WHEN NOT MATCHED THEN
  INSERT (date_key, full_date, day_of_month, month_number, quarter_number, year_number, day_name)
  VALUES (date_key, full_date, day_of_month, month_number, quarter_number, year_number, day_name);

MERGE `{project}.{clean_dataset}.dim_customer` target
USING (
  SELECT
    customer_id AS customer_key,
    customer_id,
    customer_code,
    TO_HEX(SHA256(CONCAT('{hash_salt}', ':', customer_code))) AS customer_identifier_hash,
    CONCAT(SPLIT(full_name, ' ')[SAFE_OFFSET(0)], ' ***') AS full_name_masked,
    IF(email IS NULL, NULL, CONCAT(SUBSTR(email, 1, 1), '***@', SPLIT(email, '@')[SAFE_OFFSET(1)])) AS email_masked,
    IF(phone_number IS NULL, NULL, CONCAT(REPEAT('*', GREATEST(LENGTH(REGEXP_REPLACE(phone_number, r'\D', '')) - 4, 0)), RIGHT(REGEXP_REPLACE(phone_number, r'\D', ''), 4))) AS phone_masked,
    city,
    customer_segment,
    kyc_status,
    CURRENT_TIMESTAMP() AS created_at,
    CURRENT_TIMESTAMP() AS updated_at,
    c.updated_at AS source_updated_at,
    CAST(NULL AS STRING) AS etl_run_id,
    TO_HEX(SHA256(TO_JSON_STRING(c))) AS record_hash
  FROM `{project}.{raw_dataset}.customers` c
  QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY c.updated_at DESC) = 1
) source
ON target.customer_id = source.customer_id
WHEN MATCHED AND target.record_hash IS DISTINCT FROM source.record_hash THEN UPDATE SET
  customer_code = source.customer_code,
  customer_identifier_hash = source.customer_identifier_hash,
  full_name_masked = source.full_name_masked,
  email_masked = source.email_masked,
  phone_masked = source.phone_masked,
  city = source.city,
  customer_segment = source.customer_segment,
  kyc_status = source.kyc_status,
  updated_at = CURRENT_TIMESTAMP(),
  source_updated_at = source.source_updated_at,
  etl_run_id = source.etl_run_id,
  record_hash = source.record_hash
WHEN NOT MATCHED THEN
  INSERT (customer_key, customer_id, customer_code, customer_identifier_hash, full_name_masked, email_masked, phone_masked, city, customer_segment, kyc_status, created_at, updated_at, source_updated_at, etl_run_id, record_hash)
  VALUES (customer_key, customer_id, customer_code, customer_identifier_hash, full_name_masked, email_masked, phone_masked, city, customer_segment, kyc_status, created_at, updated_at, source_updated_at, etl_run_id, record_hash);

MERGE `{project}.{clean_dataset}.dim_account` target
USING (
  SELECT
    account_id AS account_key,
    account_id,
    TO_HEX(SHA256(CONCAT('{hash_salt}', ':', account_number))) AS account_identifier_hash,
    CONCAT(REPEAT('*', GREATEST(LENGTH(account_number) - 4, 0)), RIGHT(account_number, 4)) AS masked_account_number,
    customer_id,
    branch_id,
    product_id,
    currency_code,
    account_status,
    opened_at,
    closed_at,
    CURRENT_TIMESTAMP() AS created_at,
    CURRENT_TIMESTAMP() AS updated_at,
    a.updated_at AS source_updated_at,
    CAST(NULL AS STRING) AS etl_run_id,
    TO_HEX(SHA256(TO_JSON_STRING(a))) AS record_hash
  FROM `{project}.{raw_dataset}.accounts` a
  QUALIFY ROW_NUMBER() OVER (PARTITION BY account_id ORDER BY a.updated_at DESC) = 1
) source
ON target.account_id = source.account_id
WHEN MATCHED AND target.record_hash IS DISTINCT FROM source.record_hash THEN UPDATE SET
  account_identifier_hash = source.account_identifier_hash,
  masked_account_number = source.masked_account_number,
  customer_id = source.customer_id,
  branch_id = source.branch_id,
  product_id = source.product_id,
  currency_code = source.currency_code,
  account_status = source.account_status,
  opened_at = source.opened_at,
  closed_at = source.closed_at,
  updated_at = CURRENT_TIMESTAMP(),
  source_updated_at = source.source_updated_at,
  etl_run_id = source.etl_run_id,
  record_hash = source.record_hash
WHEN NOT MATCHED THEN
  INSERT (account_key, account_id, account_identifier_hash, masked_account_number, customer_id, branch_id, product_id, currency_code, account_status, opened_at, closed_at, created_at, updated_at, source_updated_at, etl_run_id, record_hash)
  VALUES (account_key, account_id, account_identifier_hash, masked_account_number, customer_id, branch_id, product_id, currency_code, account_status, opened_at, closed_at, created_at, updated_at, source_updated_at, etl_run_id, record_hash);

MERGE `{project}.{clean_dataset}.dim_branch` target
USING (
  SELECT branch_id AS branch_key, branch_id, branch_code, branch_name, city, region, is_active,
         CURRENT_TIMESTAMP() AS created_at, CURRENT_TIMESTAMP() AS updated_at,
         b.updated_at AS source_updated_at, CAST(NULL AS STRING) AS etl_run_id,
         TO_HEX(SHA256(TO_JSON_STRING(b))) AS record_hash
  FROM `{project}.{raw_dataset}.branches` b
  QUALIFY ROW_NUMBER() OVER (PARTITION BY branch_id ORDER BY b.updated_at DESC) = 1
) source
ON target.branch_id = source.branch_id
WHEN MATCHED AND target.record_hash IS DISTINCT FROM source.record_hash THEN UPDATE SET
  branch_code = source.branch_code, branch_name = source.branch_name, city = source.city,
  region = source.region, is_active = source.is_active, updated_at = CURRENT_TIMESTAMP(),
  source_updated_at = source.source_updated_at, etl_run_id = source.etl_run_id, record_hash = source.record_hash
WHEN NOT MATCHED THEN
  INSERT (branch_key, branch_id, branch_code, branch_name, city, region, is_active, created_at, updated_at, source_updated_at, etl_run_id, record_hash)
  VALUES (branch_key, branch_id, branch_code, branch_name, city, region, is_active, created_at, updated_at, source_updated_at, etl_run_id, record_hash);

MERGE `{project}.{clean_dataset}.dim_channel` target
USING (
  SELECT channel_id AS channel_key, channel_id, channel_code, channel_name, is_active,
         CURRENT_TIMESTAMP() AS created_at, CURRENT_TIMESTAMP() AS updated_at,
         ch.updated_at AS source_updated_at, CAST(NULL AS STRING) AS etl_run_id,
         TO_HEX(SHA256(TO_JSON_STRING(ch))) AS record_hash
  FROM `{project}.{raw_dataset}.channels` ch
  QUALIFY ROW_NUMBER() OVER (PARTITION BY channel_id ORDER BY ch.updated_at DESC) = 1
) source
ON target.channel_id = source.channel_id
WHEN MATCHED AND target.record_hash IS DISTINCT FROM source.record_hash THEN UPDATE SET
  channel_code = source.channel_code, channel_name = source.channel_name, is_active = source.is_active,
  updated_at = CURRENT_TIMESTAMP(), source_updated_at = source.source_updated_at, etl_run_id = source.etl_run_id,
  record_hash = source.record_hash
WHEN NOT MATCHED THEN
  INSERT (channel_key, channel_id, channel_code, channel_name, is_active, created_at, updated_at, source_updated_at, etl_run_id, record_hash)
  VALUES (channel_key, channel_id, channel_code, channel_name, is_active, created_at, updated_at, source_updated_at, etl_run_id, record_hash);

MERGE `{project}.{clean_dataset}.dim_transaction_type` target
USING (
  SELECT transaction_type_id AS transaction_type_key, transaction_type_id, transaction_type_code,
         transaction_type_name, is_active, CURRENT_TIMESTAMP() AS created_at, CURRENT_TIMESTAMP() AS updated_at,
         tt.updated_at AS source_updated_at, CAST(NULL AS STRING) AS etl_run_id,
         TO_HEX(SHA256(TO_JSON_STRING(tt))) AS record_hash
  FROM `{project}.{raw_dataset}.transaction_types` tt
  QUALIFY ROW_NUMBER() OVER (PARTITION BY transaction_type_id ORDER BY tt.updated_at DESC) = 1
) source
ON target.transaction_type_id = source.transaction_type_id
WHEN MATCHED AND target.record_hash IS DISTINCT FROM source.record_hash THEN UPDATE SET
  transaction_type_code = source.transaction_type_code, transaction_type_name = source.transaction_type_name,
  is_active = source.is_active, updated_at = CURRENT_TIMESTAMP(), source_updated_at = source.source_updated_at,
  etl_run_id = source.etl_run_id, record_hash = source.record_hash
WHEN NOT MATCHED THEN
  INSERT (transaction_type_key, transaction_type_id, transaction_type_code, transaction_type_name, is_active, created_at, updated_at, source_updated_at, etl_run_id, record_hash)
  VALUES (transaction_type_key, transaction_type_id, transaction_type_code, transaction_type_name, is_active, created_at, updated_at, source_updated_at, etl_run_id, record_hash);

MERGE `{project}.{clean_dataset}.dim_currency` target
USING (
  SELECT FARM_FINGERPRINT(currency_code) AS currency_key, currency_code, currency_name, decimal_places, is_active,
         CURRENT_TIMESTAMP() AS created_at, CURRENT_TIMESTAMP() AS updated_at,
         cur.updated_at AS source_updated_at, CAST(NULL AS STRING) AS etl_run_id,
         TO_HEX(SHA256(TO_JSON_STRING(cur))) AS record_hash
  FROM `{project}.{raw_dataset}.currencies` cur
  QUALIFY ROW_NUMBER() OVER (PARTITION BY currency_code ORDER BY cur.updated_at DESC) = 1
) source
ON target.currency_code = source.currency_code
WHEN MATCHED AND target.record_hash IS DISTINCT FROM source.record_hash THEN UPDATE SET
  currency_name = source.currency_name, decimal_places = source.decimal_places, is_active = source.is_active,
  updated_at = CURRENT_TIMESTAMP(), source_updated_at = source.source_updated_at, etl_run_id = source.etl_run_id,
  record_hash = source.record_hash
WHEN NOT MATCHED THEN
  INSERT (currency_key, currency_code, currency_name, decimal_places, is_active, created_at, updated_at, source_updated_at, etl_run_id, record_hash)
  VALUES (currency_key, currency_code, currency_name, decimal_places, is_active, created_at, updated_at, source_updated_at, etl_run_id, record_hash);

MERGE `{project}.{clean_dataset}.dim_merchant` target
USING (
  SELECT merchant_id AS merchant_key, merchant_id, merchant_code, merchant_name, merchant_category, city, is_active,
         CURRENT_TIMESTAMP() AS created_at, CURRENT_TIMESTAMP() AS updated_at,
         m.updated_at AS source_updated_at, CAST(NULL AS STRING) AS etl_run_id,
         TO_HEX(SHA256(TO_JSON_STRING(m))) AS record_hash
  FROM `{project}.{raw_dataset}.merchants` m
  QUALIFY ROW_NUMBER() OVER (PARTITION BY merchant_id ORDER BY m.updated_at DESC) = 1
) source
ON target.merchant_id = source.merchant_id
WHEN MATCHED AND target.record_hash IS DISTINCT FROM source.record_hash THEN UPDATE SET
  merchant_code = source.merchant_code, merchant_name = source.merchant_name,
  merchant_category = source.merchant_category, city = source.city, is_active = source.is_active,
  updated_at = CURRENT_TIMESTAMP(), source_updated_at = source.source_updated_at, etl_run_id = source.etl_run_id,
  record_hash = source.record_hash
WHEN NOT MATCHED THEN
  INSERT (merchant_key, merchant_id, merchant_code, merchant_name, merchant_category, city, is_active, created_at, updated_at, source_updated_at, etl_run_id, record_hash)
  VALUES (merchant_key, merchant_id, merchant_code, merchant_name, merchant_category, city, is_active, created_at, updated_at, source_updated_at, etl_run_id, record_hash);
