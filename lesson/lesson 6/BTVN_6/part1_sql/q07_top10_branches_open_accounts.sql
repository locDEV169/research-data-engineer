-- Câu 7 (optional): Top 10 chi nhánh có nhiều tài khoản đang mở nhất.
-- Data Dictionary: account_status dùng ACTIVE / CLOSED.
-- Hiển thị: tên chi nhánh, thành phố, số tài khoản.

SELECT
    b.branch_name,
    b.city,
    COUNT(*) AS so_tai_khoan
FROM accounts AS a
INNER JOIN branches AS b
    ON b.branch_id = a.branch_id
WHERE a.account_status = 'ACTIVE'
GROUP BY b.branch_name, b.city
ORDER BY so_tai_khoan DESC
LIMIT 10;
