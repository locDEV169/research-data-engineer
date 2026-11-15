MERGE `{project}.{clean_dataset}.fact_transaction` target
USING (
  WITH latest_tx AS (
    SELECT *
    FROM `{project}.{raw_dataset}.transactions`
    QUALIFY ROW_NUMBER() OVER (PARTITION BY transaction_id ORDER BY updated_at DESC) = 1
  )
  SELECT
    tx.transaction_id AS transaction_key,
    tx.transaction_id,
    tx.transaction_reference,
    CAST(FORMAT_DATE('%Y%m%d', DATE(tx.transaction_time)) AS INT64) AS transaction_date_key,
    tx.transaction_time,
    src.account_key AS source_account_key,
    dst.account_key AS destination_account_key,
    cust.customer_key,
    br.branch_key,
    ch.channel_key,
    tt.transaction_type_key,
    cur.currency_key,
    mer.merchant_key,
    tx.amount,
    tx.fee_amount,
    tx.status AS current_status,
    tx.failure_reason,
    tx.created_at AS source_created_at,
    tx.updated_at AS source_updated_at,
    CAST(NULL AS STRING) AS etl_run_id,
    TO_HEX(SHA256(TO_JSON_STRING(tx))) AS record_hash
  FROM latest_tx tx
  LEFT JOIN `{project}.{clean_dataset}.dim_account` src ON src.account_id = tx.source_account_id
  LEFT JOIN `{project}.{clean_dataset}.dim_account` dst ON dst.account_id = tx.destination_account_id
  LEFT JOIN `{project}.{clean_dataset}.dim_customer` cust ON cust.customer_id = COALESCE(src.customer_id, dst.customer_id)
  LEFT JOIN `{project}.{clean_dataset}.dim_branch` br ON br.branch_id = tx.branch_id
  LEFT JOIN `{project}.{clean_dataset}.dim_channel` ch ON ch.channel_id = tx.channel_id
  LEFT JOIN `{project}.{clean_dataset}.dim_transaction_type` tt ON tt.transaction_type_id = tx.transaction_type_id
  LEFT JOIN `{project}.{clean_dataset}.dim_currency` cur ON cur.currency_code = tx.currency_code
  LEFT JOIN `{project}.{clean_dataset}.dim_merchant` mer ON mer.merchant_id = tx.merchant_id
) source
ON target.transaction_id = source.transaction_id
WHEN MATCHED AND target.record_hash IS DISTINCT FROM source.record_hash THEN UPDATE SET
  transaction_reference = source.transaction_reference,
  transaction_date_key = source.transaction_date_key,
  transaction_time = source.transaction_time,
  source_account_key = source.source_account_key,
  destination_account_key = source.destination_account_key,
  customer_key = source.customer_key,
  branch_key = source.branch_key,
  channel_key = source.channel_key,
  transaction_type_key = source.transaction_type_key,
  currency_key = source.currency_key,
  merchant_key = source.merchant_key,
  amount = source.amount,
  fee_amount = source.fee_amount,
  current_status = source.current_status,
  failure_reason = source.failure_reason,
  source_created_at = source.source_created_at,
  source_updated_at = source.source_updated_at,
  etl_run_id = source.etl_run_id,
  record_hash = source.record_hash,
  updated_at = CURRENT_TIMESTAMP()
WHEN NOT MATCHED THEN
  INSERT (transaction_key, transaction_id, transaction_reference, transaction_date_key, transaction_time,
          source_account_key, destination_account_key, customer_key, branch_key, channel_key,
          transaction_type_key, currency_key, merchant_key, amount, fee_amount, current_status,
          failure_reason, source_created_at, source_updated_at, etl_run_id, record_hash, created_at, updated_at)
  VALUES (transaction_key, transaction_id, transaction_reference, transaction_date_key, transaction_time,
          source_account_key, destination_account_key, customer_key, branch_key, channel_key,
          transaction_type_key, currency_key, merchant_key, amount, fee_amount, current_status,
          failure_reason, source_created_at, source_updated_at, etl_run_id, record_hash,
          CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP());

MERGE `{project}.{clean_dataset}.fact_transaction_status_event` target
USING (
  SELECT
    hist.event_id AS transaction_status_event_key,
    hist.event_id,
    ft.transaction_key,
    hist.transaction_id,
    hist.old_status,
    hist.new_status,
    hist.event_time,
    hist.source_system,
    CAST(NULL AS STRING) AS etl_run_id
  FROM `{project}.{raw_dataset}.transaction_status_history` hist
  LEFT JOIN `{project}.{clean_dataset}.fact_transaction` ft ON ft.transaction_id = hist.transaction_id
  QUALIFY ROW_NUMBER() OVER (PARTITION BY hist.event_id ORDER BY hist.updated_at DESC) = 1
) source
ON target.event_id = source.event_id
WHEN NOT MATCHED THEN
  INSERT (transaction_status_event_key, event_id, transaction_key, transaction_id, old_status,
          new_status, event_time, source_system, etl_run_id, created_at)
  VALUES (transaction_status_event_key, event_id, transaction_key, transaction_id, old_status,
          new_status, event_time, source_system, etl_run_id, CURRENT_TIMESTAMP());
