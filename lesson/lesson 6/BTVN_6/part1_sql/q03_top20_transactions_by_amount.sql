-- Câu 3: Top 20 giao dịch amount cao nhất + branch_name.
-- JOIN transactions → branches qua branch_id.
-- Hiển thị: transaction_reference, amount, branch_name, transaction_time

SELECT
    t.transaction_reference,
    t.amount,
    b.branch_name,
    t.transaction_time
FROM transactions AS t
LEFT JOIN branches AS b
    ON b.branch_id = t.branch_id
ORDER BY t.amount DESC NULLS LAST
LIMIT 20;
