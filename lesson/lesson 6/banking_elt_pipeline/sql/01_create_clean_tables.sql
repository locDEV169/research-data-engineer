CREATE TABLE IF NOT EXISTS `{project}.{clean_dataset}.dim_date` (
  date_key INT64,
  full_date DATE,
  day_of_month INT64,
  month_number INT64,
  quarter_number INT64,
  year_number INT64,
  day_name STRING
);

CREATE TABLE IF NOT EXISTS `{project}.{clean_dataset}.dim_customer` (
  customer_key INT64,
  customer_id INT64,
  customer_code STRING,
  customer_identifier_hash STRING,
  full_name_masked STRING,
  email_masked STRING,
  phone_masked STRING,
  city STRING,
  customer_segment STRING,
  kyc_status STRING,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  source_updated_at TIMESTAMP,
  etl_run_id STRING,
  record_hash STRING
);

CREATE TABLE IF NOT EXISTS `{project}.{clean_dataset}.dim_account` (
  account_key INT64,
  account_id INT64,
  account_identifier_hash STRING,
  masked_account_number STRING,
  customer_id INT64,
  branch_id INT64,
  product_id INT64,
  currency_code STRING,
  account_status STRING,
  opened_at TIMESTAMP,
  closed_at TIMESTAMP,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  source_updated_at TIMESTAMP,
  etl_run_id STRING,
  record_hash STRING
);

CREATE TABLE IF NOT EXISTS `{project}.{clean_dataset}.dim_branch` (
  branch_key INT64,
  branch_id INT64,
  branch_code STRING,
  branch_name STRING,
  city STRING,
  region STRING,
  is_active BOOL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  source_updated_at TIMESTAMP,
  etl_run_id STRING,
  record_hash STRING
);

CREATE TABLE IF NOT EXISTS `{project}.{clean_dataset}.dim_channel` (
  channel_key INT64,
  channel_id INT64,
  channel_code STRING,
  channel_name STRING,
  is_active BOOL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  source_updated_at TIMESTAMP,
  etl_run_id STRING,
  record_hash STRING
);

CREATE TABLE IF NOT EXISTS `{project}.{clean_dataset}.dim_transaction_type` (
  transaction_type_key INT64,
  transaction_type_id INT64,
  transaction_type_code STRING,
  transaction_type_name STRING,
  is_active BOOL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  source_updated_at TIMESTAMP,
  etl_run_id STRING,
  record_hash STRING
);

CREATE TABLE IF NOT EXISTS `{project}.{clean_dataset}.dim_currency` (
  currency_key INT64,
  currency_code STRING,
  currency_name STRING,
  decimal_places INT64,
  is_active BOOL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  source_updated_at TIMESTAMP,
  etl_run_id STRING,
  record_hash STRING
);

CREATE TABLE IF NOT EXISTS `{project}.{clean_dataset}.dim_merchant` (
  merchant_key INT64,
  merchant_id INT64,
  merchant_code STRING,
  merchant_name STRING,
  merchant_category STRING,
  city STRING,
  is_active BOOL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  source_updated_at TIMESTAMP,
  etl_run_id STRING,
  record_hash STRING
);

CREATE TABLE IF NOT EXISTS `{project}.{clean_dataset}.fact_transaction` (
  transaction_key INT64,
  transaction_id INT64,
  transaction_reference STRING,
  transaction_date_key INT64,
  transaction_time TIMESTAMP,
  source_account_key INT64,
  destination_account_key INT64,
  customer_key INT64,
  branch_key INT64,
  channel_key INT64,
  transaction_type_key INT64,
  currency_key INT64,
  merchant_key INT64,
  amount NUMERIC,
  fee_amount NUMERIC,
  current_status STRING,
  failure_reason STRING,
  source_created_at TIMESTAMP,
  source_updated_at TIMESTAMP,
  etl_run_id STRING,
  record_hash STRING,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `{project}.{clean_dataset}.fact_transaction_status_event` (
  transaction_status_event_key INT64,
  event_id INT64,
  transaction_key INT64,
  transaction_id INT64,
  old_status STRING,
  new_status STRING,
  event_time TIMESTAMP,
  source_system STRING,
  etl_run_id STRING,
  created_at TIMESTAMP
);
