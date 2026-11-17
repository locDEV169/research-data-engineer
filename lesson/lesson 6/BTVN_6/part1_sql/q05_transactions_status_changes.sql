-- Câu 5: transaction_id có nhiều hơn 2 lần đổi trạng thái,
-- kèm chuỗi trạng thái theo thời gian.
-- Hiển thị: transaction_id, old_status, new_status, event_time
-- Sắp xếp: transaction_id, event_time
--
-- Assumption: "một lần đổi trạng thái" = một dòng trong
-- transaction_status_history (mỗi event_id là một lần đổi).

WITH multi_change AS (
    SELECT transaction_id
    FROM transaction_status_history
    GROUP BY transaction_id
    HAVING COUNT(*) > 2
)
SELECT
    h.transaction_id,
    h.old_status,
    h.new_status,
    h.event_time
FROM transaction_status_history AS h
INNER JOIN multi_change AS m
    ON m.transaction_id = h.transaction_id
ORDER BY h.transaction_id, h.event_time;
