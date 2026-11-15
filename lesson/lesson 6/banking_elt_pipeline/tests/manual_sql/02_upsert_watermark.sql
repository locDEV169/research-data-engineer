MERGE `project-9d3c9d87-4adc-4d3b-ac1.banking_ops.watermarks` as t1
USING `project-9d3c9d87-4adc-4d3b-ac1.banking_ops.watermarks_test` as t2
on t1.source_table = t2.source_table

WHEN MATCHED THEN 
UPDATE SET t1.last_watermark_value = t2.last_watermark_value
, t1.updated_at = t2.updated_at

WHEN NOT MATCHED THEN
INSERT (source_table, last_watermark_value, updated_at)
VALUES (t2.source_table, t2.last_watermark_value, t2.updated_at)
