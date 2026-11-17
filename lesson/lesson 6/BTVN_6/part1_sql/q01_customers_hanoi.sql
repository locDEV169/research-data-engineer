-- Câu 1: Khách hàng ở Hà Nội, mới tạo trước.
-- Hiển thị: customer_code, full_name, city, customer_segment

SELECT
    customer_code,
    full_name,
    city,
    customer_segment
FROM customers
WHERE city = 'Hà Nội'
ORDER BY created_at DESC;
