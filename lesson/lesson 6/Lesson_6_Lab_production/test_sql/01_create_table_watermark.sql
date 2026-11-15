CREATE OR REPLACE TABLE `project-9d3c9d87-4adc-4d3b-ac1.banking_ops.watermarks_test` AS
SELECT * FROM
(select 'customerssss' as source_table
, TIMESTAMP('2026-08-11 09:54:30 UTC') as last_watermark_value
, TIMESTAMP('2026-08-11 11:15:30.082976 UTC') as updated_at)

