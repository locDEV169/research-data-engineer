SELECT 'duplicate_dim_customer' AS check_name, COUNT(*) AS issue_count
FROM (
  SELECT customer_id FROM `{project}.{clean_dataset}.dim_customer` GROUP BY customer_id HAVING COUNT(*) > 1
)
UNION ALL
SELECT 'duplicate_dim_account', COUNT(*)
FROM (
  SELECT account_id FROM `{project}.{clean_dataset}.dim_account` GROUP BY account_id HAVING COUNT(*) > 1
)
UNION ALL
SELECT 'duplicate_fact_transaction', COUNT(*)
FROM (
  SELECT transaction_id FROM `{project}.{clean_dataset}.fact_transaction` GROUP BY transaction_id HAVING COUNT(*) > 1
)
UNION ALL
SELECT 'duplicate_fact_status_event', COUNT(*)
FROM (
  SELECT event_id FROM `{project}.{clean_dataset}.fact_transaction_status_event` GROUP BY event_id HAVING COUNT(*) > 1
)
UNION ALL
SELECT 'null_customer_id', COUNT(*)
FROM `{project}.{clean_dataset}.dim_customer`
WHERE customer_id IS NULL
UNION ALL
SELECT 'null_account_id', COUNT(*)
FROM `{project}.{clean_dataset}.dim_account`
WHERE account_id IS NULL
UNION ALL
SELECT 'null_transaction_id', COUNT(*)
FROM `{project}.{clean_dataset}.fact_transaction`
WHERE transaction_id IS NULL
UNION ALL
SELECT 'null_event_id', COUNT(*)
FROM `{project}.{clean_dataset}.fact_transaction_status_event`
WHERE event_id IS NULL
UNION ALL
SELECT 'transaction_reconciliation', ABS(raw_count - clean_count)
FROM (
  SELECT COUNT(DISTINCT transaction_id) AS raw_count
  FROM `{project}.{raw_dataset}.transactions`
), (
  SELECT COUNT(DISTINCT transaction_id) AS clean_count
  FROM `{project}.{clean_dataset}.fact_transaction`
)
UNION ALL
SELECT 'status_event_reconciliation', ABS(raw_count - clean_count)
FROM (
  SELECT COUNT(DISTINCT event_id) AS raw_count
  FROM `{project}.{raw_dataset}.transaction_status_history`
), (
  SELECT COUNT(DISTINCT event_id) AS clean_count
  FROM `{project}.{clean_dataset}.fact_transaction_status_event`
);
