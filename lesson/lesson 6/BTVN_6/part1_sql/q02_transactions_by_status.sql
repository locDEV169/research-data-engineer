-- Câu 2: Đếm số lượng giao dịch theo từng status.
-- Hiển thị: status, so_luong

SELECT
    status,
    COUNT(*) AS so_luong
FROM transactions
GROUP BY status
ORDER BY so_luong DESC;
